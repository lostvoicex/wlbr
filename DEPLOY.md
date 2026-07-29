# 瓦力贝尔编程薄弱定位平台 · 免费部署指南

> 目标平台：**Render**（免费层）
> 部署内容：前端静态站点 + 后端 FastAPI + PostgreSQL

---

## 前置准备

1. **GitHub 仓库**：将代码推送到 GitHub 公开/私有仓库
2. **Render 账号**：访问 [render.com](https://render.com) 注册（支持 GitHub 一键登录）

---

## 第一步：修改 render.yaml 中的仓库地址

打开项目根目录的 `render.yaml`，将以下两处占位符替换为你的实际仓库地址：

```yaml
repo: https://github.com/你的用户名/你的仓库名
```

---

## 第二步：推送代码到 GitHub

```bash
git add .
git commit -m "chore: 添加 Render 部署配置"
git push origin main
```

---

## 第三步：在 Render 创建 Blueprint 部署

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 点击 **Blueprint** → **New Blueprint Instance**
3. 连接你的 GitHub 仓库
4. Render 会自动读取 `render.yaml`，预填服务配置
5. 点击 **Apply** 开始部署

Render 会依次创建：
- `wali-bell-db` — PostgreSQL 数据库（免费）
- `wali-bell-backend` — FastAPI 后端服务
- `wali-bell-frontend` — Vue 3 静态站点

---

## 第四步：初始化数据（首次部署后执行）

后端部署完成后，进入 **wali-bell-backend** 服务的 **Shell** 标签页，执行：

```bash
# 初始化演示数据（5 位学员 + 486 道题目）
python -m app.seed
```

> 注意：种子数据会清空现有题库并重新导入，仅首次部署执行。

---

## 第五步：访问你的应用

部署完成后，Render 会提供两个公网地址：

| 服务 | 地址示例 |
|------|---------|
| 前端 | `https://wali-bell-frontend.onrender.com` |
| 后端 | `https://wali-bell-backend.onrender.com` |

**默认管理员账号**：`admin` / `admin123`

---

## 免费层限制说明

| 限制项 | 说明 |
|--------|------|
| 后端休眠 | 15 分钟无请求后休眠，下次访问需 30-50 秒冷启动 |
| 数据库 | 1GB 存储，90 天后免费 PostgreSQL 会被清理 |
| 流量 | 100GB/月（前后端合计） |
| OJ 沙箱 | Render 免费层不支持 Docker，OJ 判题功能暂不可用 |

**建议**：演示/内测阶段完全够用；正式运营前迁移到付费方案。

---

## 常见问题

### Q: 前端页面刷新后 404？
A: `render.yaml` 中已配置路由回退（`/*` → `/index.html`），若仍出现请检查 Render Static Site 的 **Redirects/Rewrites** 设置。

### Q: 后端 CORS 报错？
A: 检查 `render.yaml` 中的 `CORS_ALLOW_ORIGINS` 是否正确引用了前端域名。部署后若域名变化，需在 Render Dashboard → 后端服务 → Environment 中手动更新。

### Q: 数据库连接失败？
A: Render 提供的 `DATABASE_URL` 以 `postgres://` 开头，`start.sh` 会自动转换为 `postgresql+psycopg://`。如仍失败，在 Render Dashboard → 数据库 → Info 中确认连接串。

### Q: 如何备份数据库？
A: Render 免费 PostgreSQL 90 天后会清理，建议定期执行：
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

---

## 其他部署方案

如需更快的国内访问速度，可考虑：

- **Vercel（前端）+ Render（后端）**：前端全球 CDN 加速
- **阿里云/腾讯云轻量服务器**：99 元/年，无冷启动，适合正式运营
