FROM python:3.11-slim

WORKDIR /app

# 系统依赖（含 libjpeg/zlib 供 Pillow 使用）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libffi-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY . .

# 创建数据目录（Render 持久化磁盘挂载点）
RUN mkdir -p /app/data

# 非 root 用户运行
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["bash", "start.sh"]
