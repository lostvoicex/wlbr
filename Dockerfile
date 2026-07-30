FROM python:3.10-slim

# 安装 g++ 用于 C++ 判题（可选功能）
RUN apt-get update && apt-get install -y --no-install-recommends g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存层
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 默认端口（Render/Fly.io/Koyeb 通过 PORT 环境变量注入）
ENV PORT=8000
# SQLite 数据存放到持久化卷（Fly.io）或当前目录（Render/本地）
ENV DATABASE_URL=sqlite:///./data/wali_bell.db
EXPOSE 8000

# 启动：迁移 + 种子数据初始化 + uvicorn
CMD ["bash", "start.sh"]
