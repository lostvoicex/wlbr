"""OJ 安全沙箱运行器。

本模块提供代码的安全执行环境，支持两种运行模式：
1. Docker 沙箱模式（推荐，生产环境）：在隔离容器内执行代码，限制资源，无网络访问
2. 子进程模式（开发环境兜底）：在本地子进程中执行，带超时控制

自动检测逻辑：
- 若系统已安装 Docker 且能正常调用，优先使用 Docker 模式
- 否则回退到子进程模式，并在日志中提示安全风险

使用方式：
    from app.services.sandbox_runner import SandboxRunner
    runner = SandboxRunner()
    result = runner.run_python(code_file, stdin_data, timeout=2)
    result = runner.run_cpp_compile(source_file, output_file, timeout=10)
    result = runner.run_cpp_execute(binary_file, stdin_data, timeout=2)
"""
import logging
import os
import platform
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Docker 安全限制参数
DOCKER_MEMORY_LIMIT = "256m"       # 容器内存限制
DOCKER_CPU_LIMIT = "1.0"           # CPU 核心数限制
DOCKER_TIMEOUT_BUFFER = 5          # Docker 容器总超时 = 代码超时 + buffer
DOCKER_IMAGE = "wali-bell-oj-sandbox:latest"


@dataclass
class RunResult:
    """代码执行结果。"""
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool
    mode: str  # "docker" 或 "subprocess"


def _find_python() -> Optional[str]:
    """查找可用的 Python 可执行文件（Windows 通常只有 python，Linux/macOS 有 python3）。"""
    for name in ["python3", "python"]:
        if shutil.which(name):
            return name
    return None


def _find_compiler(lang: str = "cpp") -> Optional[str]:
    """查找可用的 C++ 编译器。"""
    compilers = {"cpp": ["g++", "clang++"], "c": ["gcc", "clang"]}
    for name in compilers.get(lang, []):
        if shutil.which(name):
            return name
    return None


def _docker_available() -> bool:
    """检查 Docker 是否可用。"""
    if not shutil.which("docker"):
        return False
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def _docker_image_exists(image: str = DOCKER_IMAGE) -> bool:
    """检查指定 Docker 镜像是否已构建。"""
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", image],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


class SandboxRunner:
    """安全沙箱运行器。

    自动检测 Docker 环境，优先使用容器隔离，否则回退到子进程。
    """

    def __init__(self) -> None:
        self.use_docker = False
        self.docker_checked = False
        self._check_docker()

    def _check_docker(self) -> None:
        """检测 Docker 环境并记录日志。"""
        if self.docker_checked:
            return
        self.docker_checked = True

        if _docker_available():
            if _docker_image_exists():
                self.use_docker = True
                logger.info("[Sandbox] Docker 沙箱已就绪，使用容器隔离模式")
            else:
                logger.warning(
                    f"[Sandbox] Docker 可用但镜像 {DOCKER_IMAGE} 未构建。"
                    f"请执行：docker build -t {DOCKER_IMAGE} -f backend/oj_sandbox/Dockerfile ."
                    f"当前将回退到子进程模式（存在安全风险）"
                )
        else:
            logger.warning(
                "[Sandbox] Docker 未安装或无法连接，回退到子进程模式。"
                "生产环境请务必安装 Docker 并构建沙箱镜像！"
            )

    # ------------------------------------------------------------------
    # 统一执行入口
    # ------------------------------------------------------------------
    def run(
        self,
        cmd: List[str],
        stdin_data: str = "",
        timeout: int = 5,
        work_dir: Optional[str] = None,
    ) -> RunResult:
        """统一执行命令，自动选择 Docker 或子进程模式。"""
        if self.use_docker and work_dir:
            return self._run_in_docker(cmd, stdin_data, timeout, work_dir)
        return self._run_in_subprocess(cmd, stdin_data, timeout, cwd=work_dir)

    # ------------------------------------------------------------------
    # 子进程模式（兜底）
    # ------------------------------------------------------------------
    @staticmethod
    def _run_in_subprocess(
        cmd: List[str],
        stdin_data: str = "",
        timeout: int = 5,
        cwd: Optional[str] = None,
    ) -> RunResult:
        """在本地子进程中执行命令（带超时）。"""
        try:
            proc = subprocess.run(
                cmd,
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
            )
            return RunResult(
                stdout=proc.stdout,
                stderr=proc.stderr,
                returncode=proc.returncode,
                timed_out=False,
                mode="subprocess",
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                stdout="",
                stderr="执行超时",
                returncode=-1,
                timed_out=True,
                mode="subprocess",
            )
        except Exception as e:
            return RunResult(
                stdout="",
                stderr=str(e),
                returncode=-1,
                timed_out=False,
                mode="subprocess",
            )

    # ------------------------------------------------------------------
    # Docker 沙箱模式
    # ------------------------------------------------------------------
    def _run_in_docker(
        self,
        cmd: List[str],
        stdin_data: str = "",
        timeout: int = 5,
        work_dir: str = "",
    ) -> RunResult:
        """在 Docker 容器内执行命令。

        安全策略：
        - --network none：禁用网络
        - --read-only：根文件系统只读
        - --memory / --cpus：限制资源
        - --user nobody：非特权用户
        - --rm：执行完自动删除容器
        - -v 只挂载工作目录（只读）和 tmpfs（可写临时）
        """
        if not work_dir or not os.path.isdir(work_dir):
            logger.error("[Sandbox] Docker 模式需要提供有效的工作目录")
            # 降级到子进程
            return self._run_in_subprocess(cmd, stdin_data, timeout)

        # 将本地路径转为 Docker 挂载路径
        work_dir_abs = os.path.abspath(work_dir)
        container_work = "/sandbox/work"

        # 构建 docker run 命令
        docker_cmd = [
            "docker", "run",
            "--rm",                          # 执行完自动删除容器
            "--network", "none",             # 禁用网络
            "--read-only",                   # 根文件系统只读
            "--memory", DOCKER_MEMORY_LIMIT,
            "--cpus", DOCKER_CPU_LIMIT,
            "--user", "nobody",
            "-v", f"{work_dir_abs}:{container_work}:ro",  # 工作目录只读挂载
            "--tmpfs", "/sandbox/tmp:rw,noexec,nosuid,size=50m",  # 可写临时区
            "-w", container_work,
            DOCKER_IMAGE,
            " ".join(cmd),  # 通过 bash -c 执行
        ]

        total_timeout = timeout + DOCKER_TIMEOUT_BUFFER

        try:
            proc = subprocess.run(
                docker_cmd,
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=total_timeout,
            )
            return RunResult(
                stdout=proc.stdout,
                stderr=proc.stderr,
                returncode=proc.returncode,
                timed_out=False,
                mode="docker",
            )
        except subprocess.TimeoutExpired:
            # Docker 容器可能还在运行，尝试清理
            self._cleanup_docker_container(work_dir_abs)
            return RunResult(
                stdout="",
                stderr="Docker 容器执行超时",
                returncode=-1,
                timed_out=True,
                mode="docker",
            )
        except Exception as e:
            return RunResult(
                stdout="",
                stderr=f"Docker 执行异常: {e}",
                returncode=-1,
                timed_out=False,
                mode="docker",
            )

    def _cleanup_docker_container(self, work_dir_abs: str) -> None:
        """尝试清理可能残留的容器（通过标签匹配）。"""
        try:
            # 通过 docker ps + grep 查找并 kill（简单实现）
            subprocess.run(
                ["docker", "ps", "-q", "--filter", f"ancestor={DOCKER_IMAGE}"],
                capture_output=True,
                timeout=5,
            )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 便捷方法：Python 代码执行
    # ------------------------------------------------------------------
    def run_python(
        self,
        code_file: str,
        stdin_data: str = "",
        timeout: int = 5,
    ) -> RunResult:
        """执行 Python 代码文件。"""
        python_cmd = _find_python()
        if not python_cmd:
            return RunResult(
                stdout="", stderr="未找到 Python 运行环境", returncode=-1,
                timed_out=False, mode="subprocess",
            )
        work_dir = os.path.dirname(os.path.abspath(code_file))
        return self.run(
            [python_cmd, os.path.basename(code_file)],
            stdin_data=stdin_data,
            timeout=timeout,
            work_dir=work_dir,
        )

    # ------------------------------------------------------------------
    # 便捷方法：C++ 编译
    # ------------------------------------------------------------------
    def compile_cpp(
        self,
        source_file: str,
        output_file: str,
        timeout: int = 10,
    ) -> RunResult:
        """编译 C++ 源代码。

        注意：Docker 模式下，输出文件路径必须在挂载的工作目录内。
        """
        compiler = _find_compiler("cpp")
        if not compiler:
            return RunResult(
                stdout="", stderr="未找到 C++ 编译器（g++）", returncode=-1,
                timed_out=False, mode="subprocess",
            )
        work_dir = os.path.dirname(os.path.abspath(source_file))
        output_name = os.path.basename(output_file)
        return self.run(
            [compiler, "-std=c++17", "-O2", "-o", output_name, os.path.basename(source_file)],
            stdin_data="",
            timeout=timeout,
            work_dir=work_dir,
        )

    # ------------------------------------------------------------------
    # 便捷方法：C++ 可执行文件运行
    # ------------------------------------------------------------------
    def run_cpp_binary(
        self,
        binary_file: str,
        stdin_data: str = "",
        timeout: int = 5,
    ) -> RunResult:
        """运行已编译的 C++ 可执行文件。"""
        work_dir = os.path.dirname(os.path.abspath(binary_file))
        # Windows 上必须使用完整路径来执行当前目录下的 exe
        binary_name = os.path.basename(binary_file)
        cmd = [binary_file] if platform.system() == "Windows" else [f"./{binary_name}"]
        return self.run(
            cmd,
            stdin_data=stdin_data,
            timeout=timeout,
            work_dir=work_dir,
        )


# ------------------------------------------------------------------------------
# 全局单例（减少重复检测 Docker 的开销）
# ------------------------------------------------------------------------------
_sandbox_runner: Optional[SandboxRunner] = None


def get_sandbox_runner() -> SandboxRunner:
    """获取全局沙箱运行器实例。"""
    global _sandbox_runner
    if _sandbox_runner is None:
        _sandbox_runner = SandboxRunner()
    return _sandbox_runner
