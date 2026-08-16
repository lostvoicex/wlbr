# AGENTS.md · 项目导航

> 面向后续 Agent / 开发者的**项目全貌与规范说明**，帮助快速定位代码、避免踩坑。

## 1. 项目定位
瓦力贝尔编程薄弱定位平台。前后端分离 monorepo：`frontend/`（Vue 3 + AntDV + CodeMirror 6）、`backend/`（FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL 15），JWT 认证，RESTful API 前缀 `/api/v1`。

## 2. 快速运行
- 沙箱：`.coze` 已配好，`coze dev` 自动装依赖并起前后端。
- 本地：见 README「本地手动启动」。
- 数据库：默认 SQLite（`backend/wali_bell.db`）；PostgreSQL 通过 `docker compose up -d` 一键起。

## 3. 端口约定
- **前端 Vite**：`${DEPLOY_RUN_PORT}`（默认 5000）。**不要硬编码**。
- **后端 FastAPI**：`${BACKEND_PORT}`（默认 8000，仅沙箱内部）。
- Vite 通过 `server.proxy` 把 `/api/*` 转发到 `127.0.0.1:${BACKEND_PORT}`，浏览器只访问前端端口即可。

## 4. 关键目录 / 文件

### 后端 (`backend/`)
| 位置 | 作用 |
| --- | --- |
| `app/main.py` | FastAPI 入口，注册 CORS + 路由，SQLite dev 会自动 `create_all` |
| `app/config.py` | 环境变量读取（Pydantic Settings）|
| `app/db.py` | Engine / SessionLocal / `Base` 基类 / `get_db` 依赖 |
| `app/models/` | 11 张表 ORM：student / question / learning_record / diagnosis_session / kp_mastery_snapshot / teacher / work_order / kp_mapping / mapping_review / tab_switch_event / oj_submission |
| `app/schemas/` | 请求/响应 Pydantic：auth / student / question / diagnosis / oj |
| `app/services/mastery.py` | KP 掌握度阈值判定算法（80/50/<50 分档 + low_confidence） |
| `app/services/sb3_grader.py` | Scratch sb3 静态分析判题引擎（解析 project.json 检查 opcode） |
| `app/services/code_runner.py` | Python / C++ 代码判题引擎（集成安全沙箱：Docker 隔离优先，子进程兜底） |
| `app/services/sandbox_runner.py` | OJ 安全沙箱运行器（自动检测 Docker，限制资源/网络/用户权限） |
| `app/services/adaptive_selection.py` | 智能抽题算法（按 KP 掌握度加权：need_repair×2.5 / need_review×1.5 / mastered×0.5） |
| `app/services/retest_weighting.py` | 复测加权算法：T1×0.3 + T2×0.7 计算最终掌握度 |
| `app/core/security.py` | JWT 编解码 + bcrypt 密码哈希 |
| `app/core/deps.py` | `get_current_user`、`require_role("teacher","admin")` |
| `app/api/v1/auth.py` | 统一登录（3 种 mode：student_phone / student_id / teacher）+ refresh |
| `app/api/v1/students.py` | 学员列表 / 详情 / 新建 |
| `app/api/v1/questions.py` | 题库列表 / 抽题 / 详情 |
| `app/api/v1/diagnosis_sessions.py` | 诊断闭环：start / answer / finish / result / weighted-result + 反作弊 + 复测抽题 |
| `app/api/v1/oj.py` | OJ 编程题：problem / submit / submissions / history（支持 scratch / python / cpp） |
| `app/api/v1/kp_labels.py` | KP 标签管理（童趣化中文标签） |
| `app/api/v1/kp_mappings.py` | KP→课件映射数据 CRUD + 审核流程 |
| `app/api/v1/admin_data.py` | 数据更新通道（题目/映射的导入导出） |
| `app/api/v1/teachers.py` | 老师列表 / 详情 |
| `app/api/v1/work_orders.py` | 工单系统（映射纠错 / 资料更新申请，含 assignee_id 分配） |
| `app/api/v1/captcha.py` | 图形验证码（Pillow 生成图片 + Redis/内存缓存校验） |
| `app/api/v1/reminders.py` | 复测提醒功能 |
| `app/api/v1/copy_texts.py` | 学员端文案常量（童趣化提示语） |
| `app/seed.py` | 演示数据：5 位学员 + 486 题（Scratch L1-L4 108 + C++ L1-L8 216 + Python L1-L6 162）+ 17 条 KP 映射 |
| `app/data/` | 题库数据包：scratch_questions_data.py / cpp_questions_data.py / python_questions_data.py |
| `app/reseed_questions.py` | 开发用：只清空并重建题库（不改学员/记录） |
| `oj_sandbox/Dockerfile` | OJ 安全沙箱镜像（Alpine + python3 + g++，非 root 运行） |
| `alembic/versions/20250101_0001_initial.py` | M1 初始迁移（3 张表） |
| `alembic/versions/20250102_0002_diagnosis.py` | 第二批迁移（诊断会话 + KP 快照） |
| `alembic/versions/20250103_0003_question_explanation.py` | 第三批：question 新增 explanation 字段 |
| `alembic/versions/20250104_0004_student_note.py` | 第四批：student 新增 note / source 字段 |
| `alembic/versions/20250105_0005_question_blocks.py` | 第五批：question 新增 blocks_json（coding 题积木池） |
| `alembic/versions/20250106_0006_m2_tables.py` | 第六批：M2 表（teachers / work_orders / kp_mappings / mapping_reviews） |
| `alembic/versions/20250107_0007_oj_and_anticheat.py` | 第七批：OJ 表 + 反作弊字段（oj_submissions / tab_switch_events / 各表反作弊字段） |
| `alembic/versions/20250108_0008_work_order_assignee.py` | 第八批：work_orders 新增 assignee_id 字段（工单分配教师） |
| `app/constants/kp_labels.py` | 童趣化 KP 标签映射（Scratch 21 + Python 32 + C++ 40 = 93 条） |
| `app/core/security.py` 中 `validate_jwt_secret()` | 生产环境 JWT 密钥校验（拒绝默认值 `change-me-in-prod`） |

### 前端 (`frontend/`)
| 位置 | 作用 |
| --- | --- |
| `src/main.ts` | 入口，装配 Pinia + Router + AntDV |
| `src/App.vue` | 根组件，AntDV `ConfigProvider` 注入主题 Token（primary=#FF7A45） |
| `src/router/index.ts` | 路由 + 角色守卫（`requiresRole: student / staff`） |
| `src/stores/auth.ts` | Pinia auth store，localStorage 持久化 access/refresh token |
| `src/api/client.ts` | axios 实例，注入 Bearer，401 自动清理登录态 |
| `src/api/auth.ts`、`src/api/students.ts`、`src/api/diagnosis.ts` | 各业务 API 封装 |
| `src/views/student/StudentLogin.vue` | 学员登录（手机号+验证码 / 学号+密码 tab） |
| `src/views/student/StudentHome.vue` | 诊断入口，Scratch 1/2 级卡片选择 |
| `src/views/student/StudentDiagnosis.vue` | 学员答题页（单选/判断/积木排序/编程大题 + 进度条 + 退出拦截 + 反作弊切屏检测） |
| `src/views/student/StudentResult.vue` | 学员成绩单（徽章 + 红黄绿分区 + 复测计划 + 分享/打印） |
| `src/views/teacher/TeacherLogin.vue` | 老师登录 |
| `src/views/teacher/TeacherLayout.vue` | 老师端布局（左侧菜单 + 顶部栏） |
| `src/views/teacher/TeacherStudents.vue` | 学员列表页（分页 + 搜索 + 年级过滤） |
| `src/views/teacher/TeacherMappings.vue` | KP 映射管理（审核/编辑/章节关联） |
| `src/views/teacher/TeacherDataAdmin.vue` | 数据管理（题目/映射的导入导出/批量更新） |
| `src/views/teacher/TeacherWorkOrders.vue` | 工单处理（映射纠错 / 资料更新审核） |
| `src/components/ScratchEditor.vue` | Scratch 编程大题编辑器（TurboWarp iframe 嵌入 + postMessage 一键导出 + sb3 上传备用） |
| `src/components/CodeEditor.vue` | Python/C++ 代码编辑器（CodeMirror 6：语法高亮 + 括号匹配 + 代码折叠 + VS Code 暗色主题） |
| `src/components/CaptchaInput.vue` | 图形验证码输入组件（与后端 captcha API 对接） |
| `src/components/BrandLogo.vue` | 瓦力贝尔品牌 Logo 组件 |
| `src/styles/global.css` | 设计 Tokens（对照 `DESIGN.md`），学员端 `.kid-app` / 老师端 `.teacher-app` |

## 5. 开发约束
- **前端只能用 pnpm**：`pnpm install`、`pnpm add`；禁止 npm/yarn。
- **文案分层**：
  - 学员端（`views/student/**`）**必须**使用小朋友能看懂的口语，禁用 "session / token / 报错 / 算法 / KP" 等术语。
  - 老师端可专业化，但仍要中文化字段名（如 `session_type` → "诊断 / 复测 T1 / 复测 T2"）。
- **设计规范**：任何 UI/样式修改前先读 `DESIGN.md`；改动设计偏好时增量更新 `DESIGN.md`。
- **端口**：禁止硬编码 5000/8000；一律读环境变量 `DEPLOY_RUN_PORT` / `BACKEND_PORT`。
- **迁移**：新增/改字段走 Alembic revision，别直接改 `Base.metadata.create_all` 兜底（那是 SQLite dev 才用的兜底）。

## 6. 常见修改点导航
| 需求 | 定位 |
| --- | --- |
| 新增 API 路由 | `backend/app/api/v1/<name>.py` + 在 `app/api/__init__.py` 挂 `include_router` |
| 新增数据表 | `backend/app/models/<name>.py` + `alembic/versions/xxx_add_xxx.py` |
| 修改 JWT 密钥/过期 | `.env` 中 `JWT_*` 变量 |
| 修改老师演示账号 | `backend/app/api/v1/auth.py` `_DEMO_TEACHERS` |
| 新增前端页面 | `src/views/**` + 在 `src/router/index.ts` 注册 + 决定 `meta.requiresRole` |
| 调整主题色 | `src/styles/global.css` 顶部 Design Tokens + `src/App.vue` 的 `ConfigProvider theme` |

## 7. 测试与自检命令
- 后端导入检查：`cd backend && python -c "from app.main import app; print('ok')"`
- 前端 build（跳过类型检查）：`cd frontend && npx vite build`
- 后端接口冒烟：`curl -s http://localhost:5000/api/health`
- 运行 seed 数据：`cd backend && python -m app.seed`
- OJ 引擎单元测试：`cd backend && python -c "from app.services.code_runner import grade_code; from app.services.sb3_grader import grade_sb3; print('OJ OK')"`

## 8. 当前完成状态（截至 2026-08-16）

### 已交付
- **11 张表** 完整 ORM + Alembic 迁移链（0001→0008）
- **486 道题库** 按电子学会 2026 修订版考纲（Scratch L1-L4 / C++ L1-L8 / Python L1-L6）
- **每级 27 题**：15 单选 + 10 判断 + 2 编程大题（program）
- **OJ 判题引擎**：Scratch sb3 静态分析 + Python/C++ 运行时执行
- **OJ 安全沙箱**：Docker 容器隔离（自动检测，生产环境无 Docker 时返回 503 拒绝执行）+ 资源限制 + 网络隔离
- **反作弊系统**：切屏检测（≥3 次警告 / ≥5 次标记可疑）+ 答题时长异常检测（<3s 或 >5min）
- **复测闭环**：T1（3 天后）+ T2（7 天后），加权算法 T1×0.3 + T2×0.7
- **智能抽题**：按 KP 掌握度加权（need_repair×2.5 / need_review×1.5 / mastered×0.5）
- **数据更新通道**：admin_data API + 老师端数据管理页面
- **KP 映射审核**：二级审核流程（review_level=2 才生效）
- **工单系统**：映射纠错 / 资料更新申请，含 assignee_id 分配功能
- **前端性能优化**：chunk 拆分（vendor-vue / vendor-antdv / vendor / vendor-codemirror），index chunk 从 1.5MB 降至 7.75KB
- **童趣化 KP 标签**：93 条标签（Scratch 21 + Python 32 + C++ 40），学员端自动显示友好名称
- **图形验证码**：后端 Pillow 生成 + 前端学员/老师登录页集成
- **安全加固（P0）**：CORS 移除通配符回退 / JWT 密钥生产校验 / OJ 沙箱生产 503 / Render 持久磁盘挂载
- **编程编辑器升级**：CodeMirror 6（语法高亮 + 括号匹配 + 代码折叠）+ TurboWarp iframe 嵌入（postMessage 一键导出）

### 仍需关注（生产前）
- **Docker 沙箱镜像构建**：生产服务器需执行 `docker build -t wali-bell-oj-sandbox:latest -f backend/oj_sandbox/Dockerfile .`
- **Python/C++ 运行环境**：服务器需安装 Python 解释器和 g++ 编译器（或使用 Docker 沙箱内置环境）
- **短信验证码**：当前 student_phone 模式为占位实现（任意 4-6 位数字通过），上线前替换为真实发码服务
- **PostgreSQL 迁移**：生产环境建议使用 docker-compose.yml 中的 PostgreSQL，而非 SQLite
