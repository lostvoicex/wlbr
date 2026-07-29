"""开发用 seed 脚本：塞入演示学员 + 全量题库（18 级 × 27 题 = 486 题）+ KP 映射数据。

题库按电子学会 2026 修订版考纲出题，覆盖 3 个语言 18 个等级：
- Scratch L1-L4（4 级 × 27 题 = 108 题）
- C++     L1-L8（8 级 × 27 题 = 216 题）
- Python  L1-L6（6 级 × 27 题 = 162 题）

题目数据由 app.data 包按语言/级别分文件维护，统一汇总为 ALL_QUESTIONS。

运行：
  cd backend && python -m app.seed
"""
import json

from app.core.security import hash_password
from app.data import ALL_QUESTIONS
from app.db import Base, SessionLocal, engine
from app.models import KpMapping, Question, Student


def _coding_blocks_from_answer(answer: str) -> list[str]:
    """从 answer 的 → 分隔字符串拆出积木数组（供 coding 题 blocks_json 使用）"""
    return [s.strip() for s in answer.split("→") if s.strip()]


# =========================================================================
# KP → 奇码教材 映射数据（Scratch L1 / L2 / L3 / L4）
# 按电子学会 2026 修订版考纲
# =========================================================================
DEMO_KP_MAPPINGS = [
    # ---------- Scratch L1（6 个 KP） ----------
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "熟悉编程软件",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第1课",
        "page_ref": "8-14",
        "chapter_title": "认识 Scratch：和编程软件交朋友",
        "match_score": 95,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "角色的导入",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第2课",
        "page_ref": "16-22",
        "chapter_title": "新朋友来了：角色的导入与选择",
        "match_score": 92,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "背景的认识",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第3课",
        "page_ref": "24-30",
        "chapter_title": "舞台风景：背景的认识与切换",
        "match_score": 90,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "角色的操作",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第4课",
        "page_ref": "32-40",
        "chapter_title": "动起来吧：角色的移动、旋转与造型",
        "match_score": 94,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 4,
    },
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "声音的导入",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第5课",
        "page_ref": "42-48",
        "chapter_title": "叮叮当当：声音的导入与播放",
        "match_score": 88,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 5,
    },
    {
        "syllabus_version": "scratch-l1",
        "knowledge_point": "逻辑推理与编程数学",
        "courseware_name": "奇码星球 Scratch 一级",
        "chapter": "第6课",
        "page_ref": "50-58",
        "chapter_title": "动动小脑筋：逻辑推理与编程数学",
        "match_score": 91,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 6,
    },
    # ---------- Scratch L2（8 个 KP） ----------
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "多角色设置",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第1课",
        "page_ref": "8-14",
        "chapter_title": "角色大集合：多角色设置与互动",
        "match_score": 93,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "画笔",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第2课",
        "page_ref": "16-24",
        "chapter_title": "彩色画笔：画笔模块的妙用",
        "match_score": 90,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "选择语句",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第3课",
        "page_ref": "26-32",
        "chapter_title": "如果……就……：选择语句",
        "match_score": 91,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "循环语句",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第4课",
        "page_ref": "34-42",
        "chapter_title": "绕圈圈：循环语句",
        "match_score": 94,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 4,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "移动中的侦测",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第5课",
        "page_ref": "44-50",
        "chapter_title": "碰到了吗：移动中的侦测",
        "match_score": 89,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 5,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "运算",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第6课",
        "page_ref": "52-58",
        "chapter_title": "算一算：运算积木",
        "match_score": 88,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 6,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "声音进阶",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第7课",
        "page_ref": "60-66",
        "chapter_title": "声音变魔术：声音进阶",
        "match_score": 87,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 7,
    },
    {
        "syllabus_version": "scratch-l2",
        "knowledge_point": "逻辑推理与编程数学L2",
        "courseware_name": "奇码星球 Scratch 二级",
        "chapter": "第8课",
        "page_ref": "68-76",
        "chapter_title": "再动脑筋：逻辑推理与编程数学L2",
        "match_score": 90,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 8,
    },
    # ---------- Scratch L3（旧 L2 内容迁移：变量 / 广播消息 / 克隆 / 随机数） ----------
    {
        "syllabus_version": "scratch-l3",
        "knowledge_point": "变量",
        "courseware_name": "奇码星球 Scratch 三级",
        "chapter": "第1课",
        "page_ref": "8-14",
        "chapter_title": "会记数字的小盒子：变量",
        "match_score": 93,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "syllabus_version": "scratch-l3",
        "knowledge_point": "广播消息",
        "courseware_name": "奇码星球 Scratch 三级",
        "chapter": "第2课",
        "page_ref": "16-22",
        "chapter_title": "喊一声大家听：广播与接收",
        "match_score": 89,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "syllabus_version": "scratch-l3",
        "knowledge_point": "克隆",
        "courseware_name": "奇码星球 Scratch 三级",
        "chapter": "第3课",
        "page_ref": "24-32",
        "chapter_title": "七十二变：克隆积木",
        "match_score": 90,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 3,
    },
    {
        "syllabus_version": "scratch-l3",
        "knowledge_point": "运算-随机数",
        "courseware_name": "奇码星球 Scratch 三级",
        "chapter": "第4课",
        "page_ref": "34-40",
        "chapter_title": "神奇的骰子：随机数与运算",
        "match_score": 87,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 4,
    },
    # ---------- Scratch L4（旧 L2 内容迁移：列表 / 函数-自制积木 / 条件语句） ----------
    {
        "syllabus_version": "scratch-l4",
        "knowledge_point": "列表",
        "courseware_name": "奇码星球 Scratch 四级",
        "chapter": "第1课",
        "page_ref": "8-14",
        "chapter_title": "排排队：列表的使用",
        "match_score": 88,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "syllabus_version": "scratch-l4",
        "knowledge_point": "函数-自制积木",
        "courseware_name": "奇码星球 Scratch 四级",
        "chapter": "第2课",
        "page_ref": "16-24",
        "chapter_title": "自己做积木：函数的概念",
        "match_score": 86,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "syllabus_version": "scratch-l4",
        "knowledge_point": "条件语句",
        "courseware_name": "奇码星球 Scratch 四级",
        "chapter": "第3课",
        "page_ref": "26-34",
        "chapter_title": "如果那么否则：条件语句进阶",
        "match_score": 91,
        "source": "manual",
        "review_status": "approved",
        "review_level": 2,
        "is_active": True,
        "sort_order": 3,
    },
]


DEMO_STUDENTS = [
    {"name": "小星", "grade": 3, "phone": "13800000001", "syllabus_target": "scratch-l1", "password": "1234"},
    {"name": "小雨", "grade": 4, "phone": "13800000002", "syllabus_target": "scratch-l2", "password": "1234"},
    {"name": "阿凯", "grade": 5, "phone": "13800000003", "syllabus_target": "scratch-l2", "password": "1234"},
    {"name": "糖糖", "grade": 2, "phone": "13800000004", "syllabus_target": "scratch-l1", "password": "1234"},
    {"name": "小林", "grade": 6, "phone": "13800000005", "syllabus_target": "python-l1", "password": "1234"},
]


def upsert() -> None:
    """幂等 seed：学员用手机号判重，题目按 (syllabus_version, knowledge_point, content) 判重。

    题目数据来自 app.data.ALL_QUESTIONS（18 级 × 27 题 = 486 题）。
    """
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        # 学员
        if db.query(Student).count() == 0:
            for s in DEMO_STUDENTS:
                db.add(
                    Student(
                        name=s["name"],
                        grade=s["grade"],
                        phone=s["phone"],
                        syllabus_target=s["syllabus_target"],
                        password_hash=hash_password(s["password"]),
                    )
                )
            print(f"[seed] 插入 {len(DEMO_STUDENTS)} 个演示学员")
        else:
            print("[seed] students 表已有数据，跳过学员插入")

        # 题目：来自 app.data.ALL_QUESTIONS（18 级 × 27 题 = 486 题）
        all_questions = ALL_QUESTIONS
        existing_questions = db.query(Question).count()
        if existing_questions == 0:
            for q in all_questions:
                db.add(Question(**q))
            print(
                f"[seed] 插入 {len(all_questions)} 道演示题"
                f"（Scratch 108 + C++ 216 + Python 162 = 486）"
            )
        else:
            exist_keys = {
                (q.syllabus_version, q.knowledge_point, q.content): q
                for q in db.query(Question).all()
            }
            added = 0
            updated = 0
            for q in all_questions:
                key = (q["syllabus_version"], q["knowledge_point"], q["content"])
                if key in exist_keys:
                    # 存在则更新 answer/difficulty/explanation（用于 v1→v2 平滑升级）
                    obj = exist_keys[key]
                    obj.answer = q["answer"]
                    obj.difficulty = q["difficulty"]
                    obj.explanation = q.get("explanation")
                    # 同步更新 program 题的判题规则和语言
                    if "grading_rules" in q:
                        obj.grading_rules = q.get("grading_rules")
                    if "program_lang" in q:
                        obj.program_lang = q.get("program_lang")
                    updated += 1
                else:
                    db.add(Question(**q))
                    added += 1
            print(f"[seed] 题库：新增 {added} 道 / 更新 {updated} 道（原有 {existing_questions}）")

        # 兜底：所有 coding 题的 blocks_json 必须从 answer 回填（兼容历史数据）
        for q in db.query(Question).filter(Question.q_type == "coding").all():
            if not q.blocks_json and q.answer:
                q.blocks_json = json.dumps(
                    _coding_blocks_from_answer(q.answer), ensure_ascii=False
                )

        # KP 映射数据
        existing_mappings = db.query(KpMapping).count()
        if existing_mappings == 0:
            for m in DEMO_KP_MAPPINGS:
                db.add(KpMapping(**m))
            print(f"[seed] 插入 {len(DEMO_KP_MAPPINGS)} 条 KP 映射数据")
        else:
            exist_keys = {
                (m.syllabus_version, m.knowledge_point, m.chapter): m
                for m in db.query(KpMapping).all()
            }
            added = 0
            updated = 0
            for m in DEMO_KP_MAPPINGS:
                key = (m["syllabus_version"], m["knowledge_point"], m["chapter"])
                if key in exist_keys:
                    obj = exist_keys[key]
                    obj.courseware_name = m["courseware_name"]
                    obj.page_ref = m.get("page_ref")
                    obj.chapter_title = m.get("chapter_title")
                    obj.match_score = m.get("match_score", 0)
                    obj.sort_order = m.get("sort_order", 0)
                    updated += 1
                else:
                    db.add(KpMapping(**m))
                    added += 1
            print(f"[seed] 映射：新增 {added} 条 / 更新 {updated} 条（原有 {existing_mappings}）")

        db.commit()
    print("[seed] 完成")


# 兼容旧调用
run = upsert


if __name__ == "__main__":
    upsert()
