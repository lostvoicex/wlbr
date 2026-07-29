"""KP 童趣化命名 + 讲解词映射表（对齐电子学会 2026 修订版考纲）。

- 存储层保持技术原名不变（questions.knowledge_point / kp_mastery_snapshots.knowledge_point）
- 展示层通过本表转换为小朋友能看懂的名字 + 讲解词
- 未命中时展示层降级为原名，不 crash
"""
from typing import Dict, TypedDict


class KpLabel(TypedDict):
    original_name: str
    display_name: str
    description: str


# 原名 → (童趣化名, 讲解词)。原名为 questions 表 knowledge_point 字段的真实字符串。
KP_LABELS: Dict[str, KpLabel] = {
    # ============ L1 · Scratch 一级（电子学会考纲 6 知识块）============
    "熟悉编程软件": {
        "original_name": "熟悉编程软件",
        "display_name": "认识舞台",
        "description": "Scratch 的舞台、角色、积木和脚本区在哪里，怎么保存作品",
    },
    "角色的导入": {
        "original_name": "角色的导入",
        "display_name": "请角色上台",
        "description": "从角色库、画笔下、电脑里把小伙伴请进舞台，还能调大小",
    },
    "背景的认识": {
        "original_name": "背景的认识",
        "display_name": "搭场景",
        "description": "给舞台选一个漂亮的背景，还能切换不同背景",
    },
    "角色的操作": {
        "original_name": "角色的操作",
        "display_name": "跑跳挪动",
        "description": "让角色走路、转身、换造型、播放和停止声音",
    },
    "声音的导入": {
        "original_name": "声音的导入",
        "display_name": "放音乐",
        "description": "导入声音当背景音乐，设置音效和音量",
    },
    "逻辑推理与编程数学": {
        "original_name": "逻辑推理与编程数学",
        "display_name": "动脑小闯关",
        "description": "用逻辑推理和图形找规律，锻炼编程思维",
    },
    # ============ L2 · Scratch 二级（电子学会考纲 8 知识块）============
    "多角色设置": {
        "original_name": "多角色设置",
        "display_name": "排兵布阵",
        "description": "图层、坐标、角色大小和特效，让多个角色在舞台上各就各位",
    },
    "画笔": {
        "original_name": "画笔",
        "display_name": "魔法画笔",
        "description": "控制画笔粗细、抬笔落笔和擦除，让角色边走边画画",
    },
    "选择语句": {
        "original_name": "选择语句",
        "display_name": "如果那么",
        "description": "如果发生了什么就做什么，否则做另一件事",
    },
    "循环语句": {
        "original_name": "循环语句",
        "display_name": "重复魔法",
        "description": "重复执行、重复到某条件成立、重复固定次数",
    },
    "移动中的侦测": {
        "original_name": "移动中的侦测",
        "display_name": "碰撞雷达",
        "description": "碰到鼠标、角色、边缘或颜色时做什么，还能用键盘控制",
    },
    "运算": {
        "original_name": "运算",
        "display_name": "算术大师",
        "description": "数学运算、比较大小、逻辑运算、字符连接和四舍五入",
    },
    "声音进阶": {
        "original_name": "声音进阶",
        "display_name": "声音魔术",
        "description": "录入声音、控制音量、截取片段、设置播放时长和特效",
    },
    "逻辑推理与编程数学L2": {
        "original_name": "逻辑推理与编程数学L2",
        "display_name": "动脑进阶",
        "description": "负数、二进制、规律总结和图形推理",
    },
    # ============ L3 · Scratch 三级（保留旧 L2 内容迁移）============
    "变量": {
        "original_name": "变量",
        "display_name": "一格小盒子",
        "description": "只装一样东西的盒子，可以随时换里面装的内容",
    },
    "广播消息": {
        "original_name": "广播消息",
        "display_name": "喊话传令",
        "description": "一个角色喊一声，其他角色听到就动起来",
    },
    "克隆": {
        "original_name": "克隆",
        "display_name": "分身术",
        "description": "一个角色变出好多个自己，像下雨、放烟花那种",
    },
    "运算-随机数": {
        "original_name": "运算-随机数",
        "display_name": "掷骰子",
        "description": "每次给你一个说不准的数字，做游戏最好玩",
    },
    # ============ L4 · Scratch 四级（保留旧 L2 内容迁移）============
    "列表": {
        "original_name": "列表",
        "display_name": "多格储物盒",
        "description": "一次能装很多东西的盒子，比如全班同学的分数",
    },
    "函数-自制积木": {
        "original_name": "函数-自制积木",
        "display_name": "自制小工具",
        "description": "把一堆常用积木打包成你自己的一块积木",
    },
    "条件语句": {
        "original_name": "条件语句",
        "display_name": "如果那么进阶",
        "description": "更复杂的条件判断和嵌套选择结构",
    },
}


def get_kp_label(original_name: str) -> KpLabel:
    """按原名查童趣化标签；未命中时返回自身作为展示名，不 crash。"""
    hit = KP_LABELS.get(original_name)
    if hit is not None:
        return hit
    # 降级：未收录的 KP 展示原名即可
    return {
        "original_name": original_name,
        "display_name": original_name,
        "description": "",
    }
