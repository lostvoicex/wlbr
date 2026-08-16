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
    # ============ Python L1 ============
    "编程环境与基础语法": {
        "original_name": "编程环境与基础语法",
        "display_name": "和电脑打招呼",
        "description": "学会用 Python 写第一行代码，认识缩进和注释",
    },
    "输入输出": {
        "original_name": "输入输出",
        "display_name": "和电脑聊天",
        "description": "让电脑听你说话（输入），也能把结果告诉你（输出）",
    },
    "变量与数据类型": {
        "original_name": "变量与数据类型",
        "display_name": "魔法盒子",
        "description": "用盒子装不同的东西：整数、小数、文字等",
    },
    "数学运算": {
        "original_name": "数学运算",
        "display_name": "算术小达人",
        "description": "用加减乘除和取余让电脑帮你算数",
    },
    "Turtle绘图": {
        "original_name": "Turtle绘图",
        "display_name": "小海龟画画",
        "description": "指挥小海龟在屏幕上画各种图形",
    },
    "综合应用": {
        "original_name": "综合应用",
        "display_name": "大显身手",
        "description": "把学过的知识合在一起，做一个完整的小项目",
    },
    # ============ Python L2 ============
    "循环结构": {
        "original_name": "循环结构",
        "display_name": "转圈圈",
        "description": "让电脑自动重复做事，不用一遍遍写相同的代码",
    },
    "分支结构": {
        "original_name": "分支结构",
        "display_name": "十字路口",
        "description": "根据条件选择走哪条路：if 成立做这个，否则做那个",
    },
    "字典": {
        "original_name": "字典",
        "display_name": "名字电话本",
        "description": "用名字查找对应的电话号码，键值对应查找超快",
    },
    "元组与字符串": {
        "original_name": "元组与字符串",
        "display_name": "金手链和文字串",
        "description": "元组像金手链不能改，字符串就是一串文字",
    },
    # ============ Python L3 ============
    "排序算法": {
        "original_name": "排序算法",
        "display_name": "排排队",
        "description": "把一堆数字从小到大或从大到小排好队",
    },
    "枚举算法": {
        "original_name": "枚举算法",
        "display_name": "穷举寻宝",
        "description": "把所有可能性一个一个试，总有一款对",
    },
    "查找算法": {
        "original_name": "查找算法",
        "display_name": "大海捞针",
        "description": "在一堆数据里快速找到你想要的那一个",
    },
    "组合数据类型": {
        "original_name": "组合数据类型",
        "display_name": "数据大礼包",
        "description": "把列表、字典、集合组合在一起用",
    },
    "解析算法": {
        "original_name": "解析算法",
        "display_name": "拆解密码",
        "description": "把复杂问题拆成小步骤，一步步算出来",
    },
    # ============ Python L4 ============
    "函数定义与调用": {
        "original_name": "函数定义与调用",
        "display_name": "魔法工具箱",
        "description": "把一段代码打包成工具，要用的时候拿出来用",
    },
    "参数与返回值": {
        "original_name": "参数与返回值",
        "display_name": "快递收发",
        "description": "给工具送进去材料（参数），拿回成品（返回值）",
    },
    "异常处理": {
        "original_name": "异常处理",
        "display_name": "安全气囊",
        "description": "出错了不崩溃，提前准备好备用方案",
    },
    "文件操作": {
        "original_name": "文件操作",
        "display_name": "读写小本本",
        "description": "把数据存进文件里，下次还能读出来",
    },
    "模块与包": {
        "original_name": "模块与包",
        "display_name": "工具箱套装",
        "description": "别人写好的工具直接拿来用，不用自己造轮子",
    },
    # ============ Python L5 ============
    "math与random": {
        "original_name": "math与random",
        "display_name": "数学魔法和随机数",
        "description": "math 模块做高级数学，random 模块掷骰子",
    },
    "time模块": {
        "original_name": "time模块",
        "display_name": "时间管家",
        "description": "让程序知道现在几点，还能暂停一会儿",
    },
    "切片高级": {
        "original_name": "切片高级",
        "display_name": "切蛋糕",
        "description": "从一串数据里切出你想要的那一段",
    },
    "列表推导式": {
        "original_name": "列表推导式",
        "display_name": "一行变魔术",
        "description": "用一行代码生成一个完整的列表",
    },
    "生成器与迭代器": {
        "original_name": "生成器与迭代器",
        "display_name": "挤牙膏",
        "description": "数据不是一次全给，用一点挤一点，省内存",
    },
    "解包与星号": {
        "original_name": "解包与星号",
        "display_name": "拆礼物盒",
        "description": "用星号把一包东西拆成单个，或把单个打包成一包",
    },
    # ============ Python L6 ============
    "类与对象": {
        "original_name": "类与对象",
        "display_name": "设计图和产品",
        "description": "类是设计图，对象是按图做出来的实物",
    },
    "属性与方法": {
        "original_name": "属性与方法",
        "display_name": "特点和技能",
        "description": "对象有什么（属性），能做什么（方法）",
    },
    "继承与多态": {
        "original_name": "继承与多态",
        "display_name": "家族传承",
        "description": "爸爸会的技能孩子也会，还能各有各的绝活",
    },
    "SQLite数据库": {
        "original_name": "SQLite数据库",
        "display_name": "数据小仓库",
        "description": "用数据库存大量数据，比文件更整齐更好找",
    },
    "数据库操作": {
        "original_name": "数据库操作",
        "display_name": "仓库管理员",
        "description": "增删改查四招，管好仓库里的数据",
    },
    # ============ C++ L1 ============
    "顺序结构与程序框架": {
        "original_name": "顺序结构与程序框架",
        "display_name": "代码火车厢",
        "description": "代码从头到尾一节接一节跑，先有框架再填内容",
    },
    "输入输出 cin&cout": {
        "original_name": "输入输出 cin&cout",
        "display_name": "收发消息",
        "description": "cin 收别人发来的，cout 把你的消息发出去",
    },
    "算术运算": {
        "original_name": "算术运算",
        "display_name": "计算器小能手",
        "description": "加减乘除和取余，C++ 帮你算",
    },
    "关系运算": {
        "original_name": "关系运算",
        "display_name": "比大小裁判",
        "description": "大于小于等于，比一比谁更大",
    },
    # ============ C++ L2 ============
    "if-else 语句": {
        "original_name": "if-else 语句",
        "display_name": "岔路口选择",
        "description": "if 走这条路，else 走那条路",
    },
    "分支结构 if": {
        "original_name": "分支结构 if",
        "display_name": "如果就做",
        "description": "如果条件成立就执行，不成立就跳过",
    },
    "循环概念入门": {
        "original_name": "循环概念入门",
        "display_name": "兜圈子",
        "description": "让代码一圈一圈重复跑",
    },
    "逻辑运算": {
        "original_name": "逻辑运算",
        "display_name": "真假判断器",
        "description": "与或非三种判断，组合复杂条件",
    },
    "char 数组字符串": {
        "original_name": "char 数组字符串",
        "display_name": "字符小火车",
        "description": "一节车厢装一个字母，连起来就是一句话",
    },
    # ============ C++ L3 ============
    "for 循环": {
        "original_name": "for 循环",
        "display_name": "计数转圈圈",
        "description": "知道跑几圈就用 for，数着跑",
    },
    "while 循环": {
        "original_name": "while 循环",
        "display_name": "条件转圈圈",
        "description": "不知道跑几圈，只要条件满足就一直跑",
    },
    "一维数组": {
        "original_name": "一维数组",
        "display_name": "一排小抽屉",
        "description": "一排编了号的抽屉，每个装一个数",
    },
    "循环嵌套": {
        "original_name": "循环嵌套",
        "display_name": "套娃循环",
        "description": "大循环里套小循环，像时钟一样转",
    },
    "循环控制 break&continue": {
        "original_name": "循环控制 break&continue",
        "display_name": "急刹车和跳过",
        "description": "break 直接停，continue 跳过这一次继续",
    },
    # ============ C++ L4 ============
    "二维数组": {
        "original_name": "二维数组",
        "display_name": "格子棋盘",
        "description": "有行有列的格子，像棋盘一样存数据",
    },
    "值传递与作用域": {
        "original_name": "值传递与作用域",
        "display_name": "传话游戏",
        "description": "传的是复印件不是原件，出了门就看不到",
    },
    "简单排序": {
        "original_name": "简单排序",
        "display_name": "冒泡排队法",
        "description": "相邻两个比一比，大的往后冒",
    },
    "顺序查找": {
        "original_name": "顺序查找",
        "display_name": "从头找到尾",
        "description": "一个一个看过去，总能找到",
    },
    "递归入门": {
        "original_name": "递归入门",
        "display_name": "自己叫自己",
        "description": "函数自己调用自己，像照镜子一样",
    },
    # ============ C++ L5 ============
    "C++ string 类": {
        "original_name": "C++ string 类",
        "display_name": "超级字符串",
        "description": "比字符数组更好用的字符串工具",
    },
    "字符数组处理": {
        "original_name": "字符数组处理",
        "display_name": "字母加工厂",
        "description": "遍历、查找、替换字符数组中的字母",
    },
    "插入与快速排序": {
        "original_name": "插入与快速排序",
        "display_name": "分治排队法",
        "description": "选一个标杆，小的放左边大的放右边，递归排队",
    },
    "二分查找": {
        "original_name": "二分查找",
        "display_name": "对半砍查找",
        "description": "每次砍掉一半，快速锁定目标",
    },
    "结构体": {
        "original_name": "结构体",
        "display_name": "数据打包盒",
        "description": "把不同类型的数据打包成一个整体",
    },
    "递归进阶": {
        "original_name": "递归进阶",
        "display_name": "俄罗斯套娃",
        "description": "复杂的递归问题，像套娃一层套一层",
    },
    # ============ C++ L6 ============
    "指针基础": {
        "original_name": "指针基础",
        "display_name": "地址小纸条",
        "description": "存的是变量住在哪里的门牌号",
    },
    "栈": {
        "original_name": "栈",
        "display_name": "叠盘子",
        "description": "后放进去的先拿出来，像叠盘子一样",
    },
    "队列": {
        "original_name": "队列",
        "display_name": "排队买票",
        "description": "先排队的先买到，先进先出",
    },
    "单链表": {
        "original_name": "单链表",
        "display_name": "火车车厢",
        "description": "每节车厢知道下一节在哪，串联起来",
    },
    "贪心算法": {
        "original_name": "贪心算法",
        "display_name": "只看眼前",
        "description": "每步都选当前最好的，不后悔",
    },
    "动态规划入门": {
        "original_name": "动态规划入门",
        "display_name": "记笔记做题",
        "description": "把算过的结果记下来，不重复算",
    },
    # ============ C++ L7 ============
    "指针进阶": {
        "original_name": "指针进阶",
        "display_name": "地址魔法师",
        "description": "指针指来指去，还能指向指针",
    },
    "STL 容器": {
        "original_name": "STL 容器",
        "display_name": "百宝工具箱",
        "description": "vector、map、set 等 C++ 自带的数据结构工具",
    },
    "二叉树遍历": {
        "original_name": "二叉树遍历",
        "display_name": "家谱寻访",
        "description": "前序中序后序，三种方式拜访家族成员",
    },
    "图遍历 DFS&BFS": {
        "original_name": "图遍历 DFS&BFS",
        "display_name": "迷宫探险",
        "description": "深度优先一条路走到黑，广度优先一层层扩",
    },
    "动态规划进阶": {
        "original_name": "动态规划进阶",
        "display_name": "最优路径",
        "description": "更复杂的动态规划，找最优解",
    },
    # ============ C++ L8 ============
    "面向对象基础": {
        "original_name": "面向对象基础",
        "display_name": "造物主模式",
        "description": "设计类、创建对象，让代码像现实世界一样",
    },
    "复杂动态规划": {
        "original_name": "复杂动态规划",
        "display_name": "终极规划师",
        "description": "区间DP、树形DP等高级动态规划",
    },
    "图论算法": {
        "original_name": "图论算法",
        "display_name": "地图导航",
        "description": "最短路径、最小生成树等图论问题",
    },
    "二叉搜索树与堆": {
        "original_name": "二叉搜索树与堆",
        "display_name": "自动排队树",
        "description": "左小右大自动排好，堆是大哥在顶上",
    },
    "代码优化与工程化": {
        "original_name": "代码优化与工程化",
        "display_name": "代码装修师",
        "description": "让代码跑得快、写得整齐、好维护",
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
