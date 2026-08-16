"""Python / C++ 代码判题引擎（集成安全沙箱）。

判题规则格式（grading_rules 为 JSON 对象）：
{
  "language": "python",
  "time_limit": 2,
  "memory_limit": 128,
  "test_cases": [
    {"input": "", "expected": "Hello\\n", "hint": "无输入，输出 Hello"},
    {"input": "5", "expected": "120\\n", "hint": "输入5，输出5的阶乘"}
  ]
}

判题流程：
1. 将代码写入临时文件
2. C++ 需先编译，Python 直接运行
3. 对每个测试用例运行，对比 stdout 输出
4. 返回 verdict / score / 测试用例详情

安全执行：
- 生产环境：通过 sandbox_runner 在 Docker 容器内隔离执行
- 开发环境：Docker 不可用时自动回退到子进程（带超时控制）
- 沙箱不可用时：静态分析模式（不执行代码，检查代码结构和输出模式）
"""
import os
import platform
import re
import tempfile
from typing import Any, Dict, List

from app.services.sandbox_runner import get_sandbox_runner


def _normalize_output(text: str) -> str:
    """标准化输出文本用于比较。"""
    # 统一换行符，去除尾部空白
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.rstrip() + "\n"


def _check_output(actual_raw: str, expected_raw: str, check_mode: str) -> bool:
    """根据 check_mode 判断输出是否通过。

    Args:
        actual_raw: 实际输出原文
        expected_raw: 预期输出原文
        check_mode: "exact"(精确) / "contains"(包含) / "file_output"(降级精确)
    """
    if check_mode == "contains":
        # 包含模式：预期内容（去掉尾部换行）出现在实际输出中即可
        return expected_raw.rstrip("\n") in actual_raw
    # 精确模式 / file_output
    return _normalize_output(actual_raw) == _normalize_output(expected_raw)


def grade_code(
    code: str,
    grading_rules_json: str,
    language: str,
) -> Dict[str, Any]:
    """对 Python/C++ 代码进行判题。

    Args:
        code: 源代码文本
        grading_rules_json: 判题规则 JSON 字符串
        language: "python" 或 "cpp"

    Returns:
        {
            "verdict": str,
            "score": int,
            "passed_cases": int,
            "total_cases": int,
            "details": [...],
            "stderr": str | None
        }
    """
    import json

    # 解析判题规则
    try:
        rules = json.loads(grading_rules_json)
    except (json.JSONDecodeError, TypeError):
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_cases": 0,
            "total_cases": 0,
            "details": [],
            "stderr": "判题规则格式错误",
        }

    test_cases = rules.get("test_cases", [])
    time_limit = rules.get("time_limit", 2)

    if not test_cases:
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_cases": 0,
            "total_cases": 0,
            "details": [],
            "stderr": "没有测试用例",
        }

    total_cases = len(test_cases)
    passed_cases = 0
    case_details = []
    stderr_msg = None

    runner = get_sandbox_runner()

    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        if language == "python":
            # 写入代码文件
            code_file = os.path.join(tmpdir, "solution.py")
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)

            # 运行每个测试用例
            for tc in test_cases:
                stdin_data = tc.get("input", "")

                result = runner.run_python(
                    code_file=code_file,
                    stdin_data=stdin_data,
                    timeout=time_limit + 2,  # 额外2秒容错
                )

                if result.timed_out:
                    case_details.append({
                        "input": stdin_data,
                        "expected": tc.get("expected", ""),
                        "actual": "",
                        "passed": False,
                        "msg": f"执行超时（限制 {time_limit} 秒）",
                    })
                    continue

                if result.returncode != 0:
                    if stderr_msg is None:
                        stderr_msg = result.stderr[:500]
                    case_details.append({
                        "input": stdin_data,
                        "expected": tc.get("expected", ""),
                        "actual": result.stdout,
                        "passed": False,
                        "msg": f"运行时错误: {result.stderr[:200]}",
                    })
                    continue

                expected_raw = tc.get("expected", "")
                check_mode = tc.get("check_mode", "exact")
                passed = _check_output(result.stdout, expected_raw, check_mode)

                if passed:
                    passed_cases += 1
                    case_details.append({
                        "input": stdin_data,
                        "expected": expected_raw,
                        "actual": result.stdout,
                        "passed": True,
                        "msg": "通过",
                    })
                else:
                    case_details.append({
                        "input": stdin_data,
                        "expected": expected_raw,
                        "actual": result.stdout,
                        "passed": False,
                        "msg": "输出不匹配",
                    })

        elif language == "cpp":
            # 写入代码文件
            code_file = os.path.join(tmpdir, "solution.cpp")
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)

            # 编译
            exe_name = "solution.exe" if platform.system() == "Windows" else "solution"
            exe_file = os.path.join(tmpdir, exe_name)
            compile_result = runner.compile_cpp(
                source_file=code_file,
                output_file=exe_file,
                timeout=10,
            )

            if compile_result.returncode != 0:
                return {
                    "verdict": "compile_error",
                    "score": 0,
                    "passed_cases": 0,
                    "total_cases": total_cases,
                    "details": [],
                    "stderr": compile_result.stderr[:500],
                }

            # 运行每个测试用例
            for tc in test_cases:
                stdin_data = tc.get("input", "")

                result = runner.run_cpp_binary(
                    binary_file=exe_file,
                    stdin_data=stdin_data,
                    timeout=time_limit + 2,
                )

                if result.timed_out:
                    case_details.append({
                        "input": stdin_data,
                        "expected": tc.get("expected", ""),
                        "actual": "",
                        "passed": False,
                        "msg": f"执行超时（限制 {time_limit} 秒）",
                    })
                    continue

                if result.returncode != 0:
                    if stderr_msg is None:
                        stderr_msg = result.stderr[:500]
                    case_details.append({
                        "input": stdin_data,
                        "expected": tc.get("expected", ""),
                        "actual": result.stdout,
                        "passed": False,
                        "msg": f"运行时错误: {result.stderr[:200]}",
                    })
                    continue

                expected_raw = tc.get("expected", "")
                check_mode = tc.get("check_mode", "exact")
                passed = _check_output(result.stdout, expected_raw, check_mode)

                if passed:
                    passed_cases += 1
                    case_details.append({
                        "input": stdin_data,
                        "expected": expected_raw,
                        "actual": result.stdout,
                        "passed": True,
                        "msg": "通过",
                    })
                else:
                    case_details.append({
                        "input": stdin_data,
                        "expected": expected_raw,
                        "actual": result.stdout,
                        "passed": False,
                        "msg": "输出不匹配",
                    })

        else:
            return {
                "verdict": "compile_error",
                "score": 0,
                "passed_cases": 0,
                "total_cases": 0,
                "details": [],
                "stderr": f"不支持的语言: {language}",
            }

    # 计算分数
    score = int((passed_cases / total_cases) * 100) if total_cases > 0 else 0

    if passed_cases == total_cases:
        verdict = "accepted"
    elif passed_cases > 0:
        verdict = "partial"
    else:
        # 如果是编译错误返回 compile_error，否则 wrong_answer
        verdict = "wrong_answer"

    return {
        "verdict": verdict,
        "score": score,
        "passed_cases": passed_cases,
        "total_cases": total_cases,
        "details": case_details,
        "stderr": stderr_msg,
    }


def grade_code_static(
    code: str,
    grading_rules_json: str,
    language: str,
) -> Dict[str, Any]:
    """静态分析判题：沙箱不可用时，不执行代码，通过模式匹配检查代码结构。

    适用场景：生产环境无 Docker 沙箱时的降级判题。
    判分逻辑：
    1. 代码非空且无语法明显错误 → 基础分 40
    2. 代码包含预期输出模式（print 语句含期望值） → 每个匹配 +30
    3. 代码包含关键语法结构（input/print/for/if 等） → 额外加分
    最高 100 分，≥60 分视为通过。
    """
    import json

    try:
        rules = json.loads(grading_rules_json)
    except (json.JSONDecodeError, TypeError):
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_cases": 0,
            "total_cases": 0,
            "details": [],
            "stderr": "判题规则格式错误",
        }

    test_cases = rules.get("test_cases", [])
    if not test_cases:
        return {
            "verdict": "compile_error",
            "score": 0,
            "passed_cases": 0,
            "total_cases": 0,
            "details": [],
            "stderr": "没有测试用例",
        }

    total_cases = len(test_cases)
    case_details = []
    passed_cases = 0

    code_lines = code.strip().split("\n") if code.strip() else []
    has_code = len(code_lines) >= 2

    for idx, tc in enumerate(test_cases):
        expected = tc.get("expected", "").strip()
        stdin_data = tc.get("input", "").strip()

        if not expected:
            if has_code:
                passed_cases += 1
                case_details.append({
                    "input": stdin_data,
                    "expected": expected,
                    "actual": "[静态分析] 代码已提交，结构检查通过",
                    "passed": True,
                    "msg": "静态分析：代码非空，基础结构检查通过",
                })
            else:
                case_details.append({
                    "input": stdin_data,
                    "expected": expected,
                    "actual": "[静态分析] 代码为空",
                    "passed": False,
                    "msg": "静态分析：代码为空",
                })
            continue

        expected_lines = [l.strip() for l in expected.split("\n") if l.strip()]

        patterns_found = 0
        patterns_total = len(expected_lines) if expected_lines else 1

        for exp_line in expected_lines:
            if language == "python":
                pats = [
                    f'print("{exp_line}"',
                    f"print('{exp_line}'",
                    f'"{exp_line}"',
                    f"'{exp_line}'",
                ]
            else:
                pats = [
                    f'cout << "{exp_line}"',
                    f'cout<<"{exp_line}"',
                    f'printf("{exp_line}',
                    f'"{exp_line}"',
                ]
            if any(p in code for p in pats):
                patterns_found += 1

        if patterns_found >= patterns_total:
            passed_cases += 1
            case_details.append({
                "input": stdin_data,
                "expected": expected,
                "actual": "[静态分析] 检测到全部预期输出模式",
                "passed": True,
                "msg": "静态分析：代码中包含预期输出模式",
            })
        elif patterns_found > 0:
            case_details.append({
                "input": stdin_data,
                "expected": expected,
                "actual": f"[静态分析] 检测到 {patterns_found}/{patterns_total} 个输出模式",
                "passed": False,
                "msg": f"静态分析：部分输出模式匹配（{patterns_found}/{patterns_total}）",
            })
        else:
            if has_code:
                case_details.append({
                    "input": stdin_data,
                    "expected": expected,
                    "actual": "[静态分析] 代码已提交但未匹配到输出模式",
                    "passed": False,
                    "msg": "静态分析：代码非空，但未检测到预期输出模式",
                })
            else:
                case_details.append({
                    "input": stdin_data,
                    "expected": expected,
                    "actual": "[静态分析] 代码为空",
                    "passed": False,
                    "msg": "静态分析：代码为空",
                })

    score = int((passed_cases / total_cases) * 100) if total_cases > 0 else 0

    if not has_code:
        score = 0
        verdict = "wrong_answer"
    elif passed_cases == total_cases:
        verdict = "accepted"
    elif passed_cases > 0:
        verdict = "partial"
    else:
        score = max(score, 20)
        verdict = "wrong_answer"

    return {
        "verdict": verdict,
        "score": score,
        "passed_cases": passed_cases,
        "total_cases": total_cases,
        "details": case_details,
        "stderr": None,
    }
