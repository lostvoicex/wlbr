# 瓦力贝尔编程薄弱定位平台 · M1 骨架

面向少儿编程（小学 2-6 年级）Scratch/Python 考级学员的**查缺补漏诊断 Web 应用**。

**核心闭环**：学员做诊断题 → 系统定位薄弱知识点(KP) → 关联奇码课件章节 → 老师推补课工单 → 学员补课 → 单节点复测 T1(3 天后) + T2(7 天后) 加权评估掌握度。

---

## 目录结构

```
.
├── frontend/                # Vue 3 + Vite + AntDV + Pinia + Router
├── backend/                 # FastAPI + SQLAlchemy 2 + Alembic
│   ├── app/
│   │   ├── api/v1/          # auth / students / questions
│   │   ├── core/            # security（JWT）/ deps（鉴权）
│   │   ├── models/          # students / questions / learning_records
│   │   ├── schemas/         # Pydantic
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── seed.py          # 演示数据
│   ├── alembic/             # 迁移
│   ├── alembic.ini
│   └── requirements.txt
├── scripts/                 # 启动脚本
│   ├── start-dev.sh
│   └── start-prod.sh
├── docker-compose.yml       # PostgreSQL 15
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
python -m app.seed            # 塞入演示数据
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

## API 概览（M1）

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 健康检查 |
| POST | `/api/v1/auth/login` | 统一登录（三种 mode） |
| POST | `/api/v1/auth/refresh` | 刷新 access token |
| GET | `/api/v1/students` | 学员列表（老师/管理员，分页+搜索） |
| POST | `/api/v1/students` | 新建学员 |
| GET | `/api/v1/students/{id}` | 学员详情 |
| GET | `/api/v1/questions` | 题库列表 |
| GET | `/api/v1/questions/random` | 学员诊断抽题（M1：按大纲+级别随机取 N 道混排三型） |
| GET | `/api/v1/questions/{id}` | 题目详情 |

Swagger UI：`http://localhost:8000/docs`（沙箱代理 `http://<域名>/api/docs` 需另做转发，M1 阶段直接内部访问即可）

---

## 数据表（M1 三张）

- **students**：学员基础信息（含年级 2-6 校验、手机号唯一索引）
- **questions**：题库（single / judge / coding；`syllabus_version + grade_level` 复合索引）
- **learning_records**：作答留痕（`student_id + session_type` 复合索引）

其余 9 张表（诊断会话、工单、映射表、变式题库、KP 掌握度快照等）会在后续批次分批送入。

---

## 后续路线图

- [ ] 剩余 9 张表 DDL & Alembic 迁移
- [ ] 6 个核心算法：薄弱 KP 定位 / 复测加权（T1×0.3 + T2×0.7）/ 通过阈值判定（80%）/ 反作弊 / 映射 AI 候选 / 变式抽题
- [ ] 学员诊断答题页 + 结果报告页（薄弱 KP 高亮 + 奇码 PPT 章节页码）
- [ ] 老师工单管理 + 映射协作后台（5 档二审枚举）
- [ ] Scratch 1-2 级 76 条映射数据入库
