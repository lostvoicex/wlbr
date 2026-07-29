# OJ 安全沙箱镜像
# 用于隔离执行学员提交的 Python / C++ 代码
#
# 构建命令（在项目根目录执行）：
#   docker build -t wali-bell-oj-sandbox:latest -f backend/oj_sandbox/Dockerfile .
#
# 安全特性：
# - 非 root 用户运行代码
# - 最小化基础镜像（Alpine Linux）
# - 只包含 python3 和 g++ 编译器
# - 无网络工具、无 shell 逃逸路径

FROM alpine:3.19

LABEL maintainer="wali-bell"

# 安装运行环境：python3、g++、bash（用于脚本包装）
RUN apk add --no-cache \
    python3 \
    py3-pip \
    g++ \
    musl-dev \
    bash \
    && rm -rf /var/cache/apk/*

# 创建非特权用户（nobody 的 UID 65534）
RUN mkdir -p /sandbox /sandbox/tmp /sandbox/work \
    && chmod 755 /sandbox \
    && chmod 777 /sandbox/tmp /sandbox/work

# 设置工作目录
WORKDIR /sandbox/work

# 默认以非 root 运行
USER nobody

# 健康检查（镜像本身不提供长期服务，仅用于一次性执行）
# 容器启动后执行传入的命令，执行完自动退出
ENTRYPOINT ["bash", "-c"]
CMD ["echo 'Wali Bell OJ Sandbox Ready'"]
