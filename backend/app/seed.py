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
from app.models import KpMapping, MappingReview, Question, Student, WorkOrder


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
    # ---------- Python L1（6 个 KP） ----------
    {"syllabus_version": "python-l1", "knowledge_point": "编程环境与基础语法", "courseware_name": "奇码星球 Python 一级", "chapter": "第1课", "page_ref": "8-14", "chapter_title": "初识 Python：和电脑打招呼", "match_score": 95, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l1", "knowledge_point": "输入输出", "courseware_name": "奇码星球 Python 一级", "chapter": "第2课", "page_ref": "16-22", "chapter_title": "和电脑聊天：输入与输出", "match_score": 93, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l1", "knowledge_point": "变量与数据类型", "courseware_name": "奇码星球 Python 一级", "chapter": "第3课", "page_ref": "24-32", "chapter_title": "魔法盒子：变量与数据类型", "match_score": 94, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l1", "knowledge_point": "数学运算", "courseware_name": "奇码星球 Python 一级", "chapter": "第4课", "page_ref": "34-40", "chapter_title": "算术小达人：数学运算", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l1", "knowledge_point": "Turtle绘图", "courseware_name": "奇码星球 Python 一级", "chapter": "第5课", "page_ref": "42-50", "chapter_title": "小海龟画画：Turtle 绘图", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "python-l1", "knowledge_point": "综合应用", "courseware_name": "奇码星球 Python 一级", "chapter": "第6课", "page_ref": "52-58", "chapter_title": "大显身手：综合应用", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- Python L2（5 个 KP） ----------
    {"syllabus_version": "python-l2", "knowledge_point": "循环结构", "courseware_name": "奇码星球 Python 二级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "转圈圈：循环结构", "match_score": 93, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l2", "knowledge_point": "分支结构", "courseware_name": "奇码星球 Python 二级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "十字路口：分支结构", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l2", "knowledge_point": "列表", "courseware_name": "奇码星球 Python 二级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "一串手链：列表", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l2", "knowledge_point": "字典", "courseware_name": "奇码星球 Python 二级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "名字电话本：字典", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l2", "knowledge_point": "元组与字符串", "courseware_name": "奇码星球 Python 二级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "金手链和文字串：元组与字符串", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    # ---------- Python L3（6 个 KP） ----------
    {"syllabus_version": "python-l3", "knowledge_point": "排序算法", "courseware_name": "奇码星球 Python 三级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "排排队：排序算法", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l3", "knowledge_point": "枚举算法", "courseware_name": "奇码星球 Python 三级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "穷举寻宝：枚举算法", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l3", "knowledge_point": "查找算法", "courseware_name": "奇码星球 Python 三级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "大海捞针：查找算法", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l3", "knowledge_point": "组合数据类型", "courseware_name": "奇码星球 Python 三级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "数据大礼包：组合数据类型", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l3", "knowledge_point": "解析算法", "courseware_name": "奇码星球 Python 三级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "拆解密码：解析算法", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "python-l3", "knowledge_point": "综合应用", "courseware_name": "奇码星球 Python 三级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- Python L4（5 个 KP） ----------
    {"syllabus_version": "python-l4", "knowledge_point": "函数定义与调用", "courseware_name": "奇码星球 Python 四级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "魔法工具箱：函数定义与调用", "match_score": 93, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l4", "knowledge_point": "参数与返回值", "courseware_name": "奇码星球 Python 四级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "快递收发：参数与返回值", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l4", "knowledge_point": "异常处理", "courseware_name": "奇码星球 Python 四级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "安全气囊：异常处理", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l4", "knowledge_point": "文件操作", "courseware_name": "奇码星球 Python 四级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "读写小本本：文件操作", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l4", "knowledge_point": "模块与包", "courseware_name": "奇码星球 Python 四级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "工具箱套装：模块与包", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    # ---------- Python L5（7 个 KP） ----------
    {"syllabus_version": "python-l5", "knowledge_point": "math与random", "courseware_name": "奇码星球 Python 五级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "数学魔法和随机数：math 与 random", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l5", "knowledge_point": "time模块", "courseware_name": "奇码星球 Python 五级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "时间管家：time 模块", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l5", "knowledge_point": "切片高级", "courseware_name": "奇码星球 Python 五级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "切蛋糕：切片高级", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l5", "knowledge_point": "列表推导式", "courseware_name": "奇码星球 Python 五级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "一行变魔术：列表推导式", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l5", "knowledge_point": "生成器与迭代器", "courseware_name": "奇码星球 Python 五级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "挤牙膏：生成器与迭代器", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "python-l5", "knowledge_point": "解包与星号", "courseware_name": "奇码星球 Python 五级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "拆礼物盒：解包与星号", "match_score": 84, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    {"syllabus_version": "python-l5", "knowledge_point": "综合应用", "courseware_name": "奇码星球 Python 五级", "chapter": "第7课", "page_ref": "68-76", "chapter_title": "大显身手：综合应用", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 7},
    # ---------- Python L6（6 个 KP） ----------
    {"syllabus_version": "python-l6", "knowledge_point": "类与对象", "courseware_name": "奇码星球 Python 六级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "设计图和产品：类与对象", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "python-l6", "knowledge_point": "属性与方法", "courseware_name": "奇码星球 Python 六级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "特点和技能：属性与方法", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "python-l6", "knowledge_point": "继承与多态", "courseware_name": "奇码星球 Python 六级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "家族传承：继承与多态", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "python-l6", "knowledge_point": "SQLite数据库", "courseware_name": "奇码星球 Python 六级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "数据小仓库：SQLite 数据库", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "python-l6", "knowledge_point": "数据库操作", "courseware_name": "奇码星球 Python 六级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "仓库管理员：数据库操作", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "python-l6", "knowledge_point": "综合应用", "courseware_name": "奇码星球 Python 六级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- C++ L1（6 个 KP） ----------
    {"syllabus_version": "cpp-l1", "knowledge_point": "顺序结构与程序框架", "courseware_name": "奇码星球 C++ 一级", "chapter": "第1课", "page_ref": "8-14", "chapter_title": "代码火车厢：顺序结构与程序框架", "match_score": 95, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l1", "knowledge_point": "输入输出 cin&cout", "courseware_name": "奇码星球 C++ 一级", "chapter": "第2课", "page_ref": "16-22", "chapter_title": "收发消息：输入输出 cin&cout", "match_score": 93, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l1", "knowledge_point": "变量与数据类型", "courseware_name": "奇码星球 C++ 一级", "chapter": "第3课", "page_ref": "24-30", "chapter_title": "魔法盒子：变量与数据类型", "match_score": 94, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l1", "knowledge_point": "算术运算", "courseware_name": "奇码星球 C++ 一级", "chapter": "第4课", "page_ref": "32-38", "chapter_title": "计算器小能手：算术运算", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l1", "knowledge_point": "关系运算", "courseware_name": "奇码星球 C++ 一级", "chapter": "第5课", "page_ref": "40-46", "chapter_title": "比大小裁判：关系运算", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l1", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 一级", "chapter": "第6课", "page_ref": "48-54", "chapter_title": "大显身手：综合应用", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- C++ L2（6 个 KP） ----------
    {"syllabus_version": "cpp-l2", "knowledge_point": "分支结构 if", "courseware_name": "奇码星球 C++ 二级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "如果就做：分支结构 if", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l2", "knowledge_point": "if-else 语句", "courseware_name": "奇码星球 C++ 二级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "岔路口选择：if-else 语句", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l2", "knowledge_point": "逻辑运算", "courseware_name": "奇码星球 C++ 二级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "真假判断器：逻辑运算", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l2", "knowledge_point": "循环概念入门", "courseware_name": "奇码星球 C++ 二级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "兜圈子：循环概念入门", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l2", "knowledge_point": "char 数组字符串", "courseware_name": "奇码星球 C++ 二级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "字符小火车：char 数组字符串", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l2", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 二级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- C++ L3（6 个 KP） ----------
    {"syllabus_version": "cpp-l3", "knowledge_point": "for 循环", "courseware_name": "奇码星球 C++ 三级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "计数转圈圈：for 循环", "match_score": 93, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l3", "knowledge_point": "while 循环", "courseware_name": "奇码星球 C++ 三级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "条件转圈圈：while 循环", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l3", "knowledge_point": "一维数组", "courseware_name": "奇码星球 C++ 三级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "一排小抽屉：一维数组", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l3", "knowledge_point": "循环嵌套", "courseware_name": "奇码星球 C++ 三级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "套娃循环：循环嵌套", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l3", "knowledge_point": "循环控制 break&continue", "courseware_name": "奇码星球 C++ 三级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "急刹车和跳过：循环控制 break&continue", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l3", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 三级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- C++ L4（7 个 KP） ----------
    {"syllabus_version": "cpp-l4", "knowledge_point": "二维数组", "courseware_name": "奇码星球 C++ 四级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "格子棋盘：二维数组", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l4", "knowledge_point": "值传递与作用域", "courseware_name": "奇码星球 C++ 四级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "传话游戏：值传递与作用域", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l4", "knowledge_point": "函数定义与调用", "courseware_name": "奇码星球 C++ 四级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "魔法工具箱：函数定义与调用", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l4", "knowledge_point": "简单排序", "courseware_name": "奇码星球 C++ 四级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "冒泡排队法：简单排序", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l4", "knowledge_point": "顺序查找", "courseware_name": "奇码星球 C++ 四级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "从头找到尾：顺序查找", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l4", "knowledge_point": "递归入门", "courseware_name": "奇码星球 C++ 四级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "自己叫自己：递归入门", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    {"syllabus_version": "cpp-l4", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 四级", "chapter": "第7课", "page_ref": "68-76", "chapter_title": "大显身手：综合应用", "match_score": 84, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 7},
    # ---------- C++ L5（7 个 KP） ----------
    {"syllabus_version": "cpp-l5", "knowledge_point": "C++ string 类", "courseware_name": "奇码星球 C++ 五级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "超级字符串：C++ string 类", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l5", "knowledge_point": "字符数组处理", "courseware_name": "奇码星球 C++ 五级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "字母加工厂：字符数组处理", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l5", "knowledge_point": "插入与快速排序", "courseware_name": "奇码星球 C++ 五级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "分治排队法：插入与快速排序", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l5", "knowledge_point": "二分查找", "courseware_name": "奇码星球 C++ 五级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "对半砍查找：二分查找", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l5", "knowledge_point": "结构体", "courseware_name": "奇码星球 C++ 五级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "数据打包盒：结构体", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l5", "knowledge_point": "递归进阶", "courseware_name": "奇码星球 C++ 五级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "俄罗斯套娃：递归进阶", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    {"syllabus_version": "cpp-l5", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 五级", "chapter": "第7课", "page_ref": "68-76", "chapter_title": "大显身手：综合应用", "match_score": 84, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 7},
    # ---------- C++ L6（7 个 KP） ----------
    {"syllabus_version": "cpp-l6", "knowledge_point": "指针基础", "courseware_name": "奇码星球 C++ 六级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "地址小纸条：指针基础", "match_score": 92, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l6", "knowledge_point": "栈", "courseware_name": "奇码星球 C++ 六级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "叠盘子：栈", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l6", "knowledge_point": "队列", "courseware_name": "奇码星球 C++ 六级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "排队买票：队列", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l6", "knowledge_point": "单链表", "courseware_name": "奇码星球 C++ 六级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "火车车厢：单链表", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l6", "knowledge_point": "贪心算法", "courseware_name": "奇码星球 C++ 六级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "只看眼前：贪心算法", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l6", "knowledge_point": "动态规划入门", "courseware_name": "奇码星球 C++ 六级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "记笔记做题：动态规划入门", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    {"syllabus_version": "cpp-l6", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 六级", "chapter": "第7课", "page_ref": "68-76", "chapter_title": "大显身手：综合应用", "match_score": 83, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 7},
    # ---------- C++ L7（6 个 KP） ----------
    {"syllabus_version": "cpp-l7", "knowledge_point": "指针进阶", "courseware_name": "奇码星球 C++ 七级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "地址魔法师：指针进阶", "match_score": 90, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l7", "knowledge_point": "STL 容器", "courseware_name": "奇码星球 C++ 七级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "百宝工具箱：STL 容器", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l7", "knowledge_point": "二叉树遍历", "courseware_name": "奇码星球 C++ 七级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "家谱寻访：二叉树遍历", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l7", "knowledge_point": "图遍历 DFS&BFS", "courseware_name": "奇码星球 C++ 七级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "迷宫探险：图遍历 DFS&BFS", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l7", "knowledge_point": "动态规划进阶", "courseware_name": "奇码星球 C++ 七级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "最优路径：动态规划进阶", "match_score": 86, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l7", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 七级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 84, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
    # ---------- C++ L8（6 个 KP） ----------
    {"syllabus_version": "cpp-l8", "knowledge_point": "二叉搜索树与堆", "courseware_name": "奇码星球 C++ 八级", "chapter": "第1课", "page_ref": "8-16", "chapter_title": "自动排队树：二叉搜索树与堆", "match_score": 91, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 1},
    {"syllabus_version": "cpp-l8", "knowledge_point": "面向对象基础", "courseware_name": "奇码星球 C++ 八级", "chapter": "第2课", "page_ref": "18-26", "chapter_title": "造物主模式：面向对象基础", "match_score": 89, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 2},
    {"syllabus_version": "cpp-l8", "knowledge_point": "图论算法", "courseware_name": "奇码星球 C++ 八级", "chapter": "第3课", "page_ref": "28-36", "chapter_title": "地图导航：图论算法", "match_score": 88, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 3},
    {"syllabus_version": "cpp-l8", "knowledge_point": "复杂动态规划", "courseware_name": "奇码星球 C++ 八级", "chapter": "第4课", "page_ref": "38-46", "chapter_title": "终极规划师：复杂动态规划", "match_score": 87, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 4},
    {"syllabus_version": "cpp-l8", "knowledge_point": "代码优化与工程化", "courseware_name": "奇码星球 C++ 八级", "chapter": "第5课", "page_ref": "48-56", "chapter_title": "代码装修师：代码优化与工程化", "match_score": 85, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 5},
    {"syllabus_version": "cpp-l8", "knowledge_point": "综合应用", "courseware_name": "奇码星球 C++ 八级", "chapter": "第6课", "page_ref": "58-66", "chapter_title": "大显身手：综合应用", "match_score": 83, "source": "manual", "review_status": "approved", "review_level": 2, "is_active": True, "sort_order": 6},
]


DEMO_WORK_ORDERS = [
    {
        "student_id": 1,
        "syllabus_target": "scratch-l1",
        "weak_kps": "声音的导入",
        "title": "小星的补课工单：声音导入专题",
        "description": "根据诊断结果，小星在「声音的导入」知识点上需要加强。建议复习第5课内容，练习导入不同格式的声音文件并设置播放。",
        "chapters_json": json.dumps([{"chapter": "第5课", "page_ref": "42-48", "title": "叮叮当当：声音的导入与播放"}], ensure_ascii=False),
        "status": "pending",
        "priority": "high",
    },
    {
        "student_id": 2,
        "syllabus_target": "scratch-l2",
        "weak_kps": "运算,声音进阶",
        "title": "小雨的补课工单：运算与声音进阶",
        "description": "小雨在「运算」和「声音进阶」两个知识点上掌握不够扎实，建议结合课件第6课和第7课进行针对性练习。",
        "chapters_json": json.dumps([
            {"chapter": "第6课", "page_ref": "52-58", "title": "算一算：运算积木"},
            {"chapter": "第7课", "page_ref": "60-66", "title": "声音变魔术：声音进阶"},
        ], ensure_ascii=False),
        "status": "in_progress",
        "priority": "medium",
    },
    {
        "student_id": 3,
        "syllabus_target": "scratch-l2",
        "weak_kps": "循环语句",
        "title": "阿凯的补课工单：循环语句巩固",
        "description": "阿凯在循环语句的理解上存在偏差，已完成补课练习并通过复测。",
        "chapters_json": json.dumps([{"chapter": "第4课", "page_ref": "34-42", "title": "绕圈圈：循环语句"}], ensure_ascii=False),
        "status": "completed",
        "priority": "medium",
    },
    {
        "student_id": 5,
        "syllabus_target": "python-l1",
        "weak_kps": "Turtle绘图,数学运算",
        "title": "小林的补课工单：Turtle 绘图与数学运算",
        "description": "小林在 Python 一级的 Turtle 绘图和数学运算方面需要加强，建议结合课件第4课和第5课练习。",
        "chapters_json": json.dumps([
            {"chapter": "第4课", "page_ref": "34-40", "title": "算术小达人：数学运算"},
            {"chapter": "第5课", "page_ref": "42-50", "title": "小海龟画画：Turtle 绘图"},
        ], ensure_ascii=False),
        "status": "pending",
        "priority": "high",
    },
]

DEMO_MAPPING_REVIEWS = [
    {
        "mapping_id": 1,
        "reviewer_id": None,
        "review_round": 1,
        "result": "approved",
        "review_level": 1,
        "note": "映射准确，知识点与课件章节对应正确",
    },
    {
        "mapping_id": 1,
        "reviewer_id": None,
        "review_round": 2,
        "result": "approved",
        "review_level": 2,
        "note": "二审通过，映射生效",
    },
    {
        "mapping_id": 2,
        "reviewer_id": None,
        "review_round": 1,
        "result": "approved",
        "review_level": 1,
        "note": "映射合理",
    },
    {
        "mapping_id": 2,
        "reviewer_id": None,
        "review_round": 2,
        "result": "approved",
        "review_level": 2,
        "note": "二审通过",
    },
    {
        "mapping_id": 3,
        "reviewer_id": None,
        "review_round": 1,
        "result": "needs_review",
        "review_level": 1,
        "note": "页码范围需要核实，建议确认具体页数",
    },
    {
        "mapping_id": 3,
        "reviewer_id": None,
        "review_round": 2,
        "result": "approved",
        "review_level": 2,
        "note": "已核实页码，二审通过",
    },
]


DEMO_STUDENTS = [
    {"name": "小星", "grade": 3, "phone": "13800000001", "syllabus_target": "scratch-l1", "password": "1234"},
    {"name": "小雨", "grade": 4, "phone": "13800000002", "syllabus_target": "scratch-l2", "password": "1234"},
    {"name": "阿凯", "grade": 5, "phone": "13800000003", "syllabus_target": "scratch-l2", "password": "1234"},
    {"name": "糖糖", "grade": 2, "phone": "13800000004", "syllabus_target": "scratch-l1", "password": "1234"},
    {"name": "小林", "grade": 6, "phone": "13800000005", "syllabus_target": "python-l1", "password": "1234"},
    {"name": "小峰", "grade": 5, "phone": "13800000006", "syllabus_target": "cpp-l1", "password": "1234"},
    {"name": "朵朵", "grade": 4, "phone": "13800000007", "syllabus_target": "python-l2", "password": "1234"},
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

        # 演示工单
        existing_wo = db.query(WorkOrder).count()
        if existing_wo == 0:
            for wo in DEMO_WORK_ORDERS:
                db.add(WorkOrder(**wo))
            print(f"[seed] 插入 {len(DEMO_WORK_ORDERS)} 条演示工单")
        else:
            print(f"[seed] 工单表已有 {existing_wo} 条，跳过")

        # 映射审核记录
        existing_mr = db.query(MappingReview).count()
        if existing_mr == 0:
            for mr in DEMO_MAPPING_REVIEWS:
                db.add(MappingReview(**mr))
            print(f"[seed] 插入 {len(DEMO_MAPPING_REVIEWS)} 条审核记录")
        else:
            print(f"[seed] 审核记录已有 {existing_mr} 条，跳过")

        db.commit()
    print("[seed] 完成")


# 兼容旧调用
run = upsert


if __name__ == "__main__":
    upsert()
