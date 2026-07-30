name: 部署前端到 GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'
      - '.github/workflows/deploy-frontend.yml'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: 检出代码
        uses: actions/checkout@v4

      - name: 安装 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: 安装依赖
        working-directory: frontend
        run: npm install

      - name: 构建
        working-directory: frontend
        run: npx vite build
        env:
          VITE_API_BASE_URL: https://wali-bell-backend.fly.dev/api/v1

      - name: 设置 Pages
        uses: actions/configure-pages@v4

      - name: 上传构建产物
        uses: actions/upload-pages-artifact@v3
        with:
          path: frontend/dist

      - name: 部署到 GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4