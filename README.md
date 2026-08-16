# 瓦力贝尔编程薄弱定位平台

面向少儿编程（小学 2-6 年级）Scratch / Python / C++ 考级学员的**查缺补漏诊断 Web 应用**。

**核心闭环**：学员做诊断题 → 系统定位薄弱知识点(KP) → 关联课件章节 → 老师推补课工单 → 学员补课 → 单节点复测 T1(3 天后) + T2(7 天后) 加权评估掌握度。

---

## 目录结构

```
.
├── frontend/                # Vue 3 + Vite + AntDV + Pinia + CodeMirror 6
├── backend/                 # FastAPI + SQLAlchemy 2 + Alembic
│   ├── app/
│   │   ├── api/v1/          # 13 个路由模块
│   │   ├── core/            # security（JWT + bcrypt）/ deps（鉴权）
│   │   ├── models/          # 11 张表 ORM
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 6 个核心算法服务
│   │   ├── constants/       # KP 标签映射（93 条童趣化标签）
│   │   ├── data/            # 题库数据包（486 题）
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── seed.py          # 演示数据
│   ├── alembic/             # 迁移链 0001→0008
│   ├── oj_sandbox/          # OJ 安全沙箱 Docker 镜像
│   └── requirements.txt
├── scripts/                 # 启动脚本
│   ├── start-dev.sh
│   └── start-prod.sh
├── docker-compose.yml       # PostgreSQL 15
├── render.yaml              # Render 部署配置（含持久磁盘）
├── .env.example
├── .coze                    # 沙箱环境入口
├── DESIGN.md                # 设计规范
└── AGENTS.md                # Agent 项目导航
```

---

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
```

默认使用 SQLite（`sqlite:///./wali_bell.db`），零依赖启动即可。

如需切换到 PostgreSQL 15：

```bash
docker compose up -d
# 将 .env 中 DATABASE_URL 改为：
# postgresql+psycopg://wali:wali_pwd@localhost:5432/wali_bell
```

### 2. 一键启动（沙箱环境）

沙箱环境下 `.coze` 已配置好：`coze dev` 会自动 `pnpm install` + `pip install -r requirements.txt` 并跑起前后端。前端监听 `${DEPLOY_RUN_PORT}`（默认 5000），后端固定内部 8000，Vite `/api` 代理转发。

### 3. 本地手动启动

```bash
# 后端
cd backend
pip install -r requirements.txt
alembic upgrade head          # 使用 PostgreSQL 时执行；SQLite 首次由 create_all 兜底
python -m app.seed            # 塞入演示数据（486 题 + 5 位学员 + 17 条映射）
uvicorn app.main:app --reload --port 8000

# 前端（新终端）
cd frontend
pnpm install
pnpm dev                       # 默认 5000
```

访问：http://localhost:5000

---

## 演示账号

### 学员端
- 手机号登录：`13800000001` / 验证码：随便 4-6 位数字（如 `1234`）
- 学号登录：学员 ID `1` / 密码 `1234`（seed 数据共 5 位小朋友，ID 1-5）

### 老师端
- 老师：`T001` / `teacher123`（还有 `T002`）
- 管理员：`admin` / `admin123`

---

## API 概览

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 健康检查 |
| GET | `/api/v1/captcha/image` | 获取图形验证码 |
| POST | `/api/v1/captcha/verify` | 校验验证码 |
| POST | `/api/v1/auth/login` | 统一登录（三种 mode：student_phone / student_id / teacher） |
| POST | `/api/v1/auth/refresh` | 刷新 access token |
| GET | `/api/v1/students` | 学员列表（分页 + 搜索 + 年级过滤） |
| POST | `/api/v1/students` | 新建学员 |
| GET | `/api/v1/students/{id}` | 学员详情 |
| GET | `/api/v1/questions` | 题库列表（分页 + 过滤） |
| GET | `/api/v1/questions/random` | 学员诊断抽题 |
| GET | `/api/v1/questions/{id}` | 题目详情 |
| POST | `/api/v1/diagnosis/start` | 开始诊断会话 |
| POST | `/api/v1/diagnosis/{id}/answer` | 提交单题答案 |
| POST | `/api/v1/diagnosis/{id}/finish` | 结束诊断并生成报告 |
| GET | `/api/v1/diagnosis/{id}/result` | 获取诊断结果 |
| GET | `/api/v1/diagnosis/{id}/weighted-result` | 获取复测加权结果 |
| GET | `/api/v1/oj/problem/{id}` | 获取编程题详情 |
| POST | `/api/v1/oj/submit` | 提交编程题判题（scratch / python / cpp） |
| GET | `/api/v1/oj/submissions` | 提交记录列表 |
| GET | `/api/v1/oj/history` | 历史提交 |
| GET | `/api/v1/kp-labels` | KP 标签列表（童趣化） |
| GET | `/api/v1/kp-mappings` | KP→课件映射列表 |
| POST | `/api/v1/kp-mappings` | 新建映射 |
| PUT | `/api/v1/kp-mappings/{id}/review` | 映射审核（一审/二审） |
| GET | `/api/v1/work-orders` | 工单列表（分页 + 筛选） |
| POST | `/api/v1/work-orders` | 创建工单 |
| GET | `/api/v1/work-orders/{id}` | 工单详情 |
| PUT | `/api/v1/work-orders/{id}` | 更新工单 |
| POST | `/api/v1/work-orders/{id}/complete` | 标记工单完成 |
| GET | `/api/v1/teachers` | 老师列表 |
| GET | `/api/v1/admin/data/questions` | 题库导出 |
| POST | `/api/v1/admin/data/questions` | 题库导入/批量更新 |
| GET | `/api/v1/admin/data/mappings` | 映射导出 |
| POST | `/api/v1/admin/data/mappings` | 映射导入/批量更新 |

Swagger UI：`http://localhost:8000/docs`

---

## 数据表（11 张）

| 表 | 说明 | 关键索引 |
| --- | --- | --- |
| **students** | 学员基础信息 | phone 唯一索引 |
| **questions** | 题库（486 题） | syllabus_version + grade_level 复合索引 |
| **learning_records** | 作答留痕 | student_id + session_type 复合索引 |
| **diagnosis_sessions** | 诊断/复测会话 | student_id 索引 |
| **kp_mastery_snapshots** | KP 掌握度快照 | session_id 索引 |
| **teachers** | 老师/管理员账号 | teacher_no 唯一索引 |
| **work_orders** | 补课工单 | student_id / status / assignee_id 索引 |
| **kp_mappings** | KP→课件映射 | syllabus_version + knowledge_point 复合索引 |
| **mapping_reviews** | 映射审核记录 | mapping_id 索引 |
| **tab_switch_events** | 切屏事件（反作弊） | session_id 索引 |
| **oj_submissions** | OJ 编程题提交记录 | student_id + question_id / session_id 索引 |

---

## 核心算法

| 算法 | 位置 | 说明 |
| --- | --- | --- |
| KP 掌握度阈值判定 | `app/services/mastery.py` | ≥80 mastered / ≥50 need_review / <50 need_repair + low_confidence |
| 智能抽题 | `app/services/adaptive_selection.py` | 按 KP 掌握度加权：need_repair×2.5 / need_review×1.5 / mastered×0.5 |
| 复测加权 | `app/services/retest_weighting.py` | T1×0.3 + T2×0.7 |
| Scratch 判题 | `app/services/sb3_grader.py` | sb3 静态分析：解析 project.json 检查 opcode 规则 |
| Python/C++ 判题 | `app/services/code_runner.py` | 运行时执行：编译 + 逐测试用例对比 stdout |
| 安全沙箱 | `app/services/sandbox_runner.py` | Docker 容器隔离 + 资源限制 + 网络隔离 |

---

## 安全特性

- **JWT 认证**：bcrypt 密码哈希 + access/refresh token 双令牌
- **角色权限**：student / teacher / admin 三级，路由级守卫
- **图形验证码**：Pillow 生成 + 登录页集成
- **CORS 安全**：严格白名单，无通配符回退
- **JWT 密钥校验**：生产环境拒绝默认密钥 `change-me-in-prod`
- **OJ 安全沙箱**：Docker 容器隔离（生产无 Docker 返回 503）+ 资源限制 + 网络隔离
- **反作弊系统**：切屏检测（≥3 次警告 / ≥5 次标记可疑）+ 答题时长异常检测（<3s 或 >5min）

---

## 前端特性

- **Vue 3 + AntDV**：主题色 #FF7A45（瓦力橙）
- **CodeMirror 6**：Python/C++ 语法高亮 + 括号匹配 + 代码折叠 + VS Code 暗色主题
- **TurboWarp 集成**：iframe 嵌入 + postMessage 一键导出 .sb3 文件
- **chunk 拆分**：vendor-vue / vendor-antdv / vendor / vendor-codemirror，index chunk 仅 7.75KB
- **童趣化 UI**：学员端口语文案，禁用技术术语

---

## 生产部署

### Render（推荐）
```bash
# render.yaml 已配置：后端 Web Service + 持久磁盘
# 前端构建为静态文件，部署到 GitHub Pages
```

### Docker Compose
```bash
docker compose up -d           # 启动 PostgreSQL 15
docker build -t wali-bell-oj-sandbox:latest -f backend/oj_sandbox/Dockerfile .
```

### 生产环境检查清单
- [ ] 设置 `JWT_SECRET_KEY` 为非默认值
- [ ] 设置 `APP_ENV=prod`（启用 OJ 沙箱 503 拒绝、JWT 密钥校验）
- [ ] 配置 `CORS_ORIGINS` 为前端域名（不要用通配符）
- [ ] 构建 OJ 沙箱镜像：`docker build -t wali-bell-oj-sandbox:latest -f backend/oj_sandbox/Dockerfile .`
- [ ] 安装 Python 解释器和 g++ 编译器（或使用 Docker 沙箱内置环境）
- [ ] 替换短信验证码占位实现为真实发码服务
- [ ] 切换到 PostgreSQL（生产不建议用 SQLite）
