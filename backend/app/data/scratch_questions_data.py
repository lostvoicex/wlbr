"""Scratch L1-L4 题库数据（按电子学会 2026 修订版考纲）。

共 4 级 × 27 题 = 108 题
每级题型分布：15 单选(single) + 10 判断(judge) + 2 编程(program/coding)

考纲对齐（电子学会青少年软件编程（图形化）等级考试标准 2026 修订版）：
- L1（2-3 年级·入门）：熟悉编程软件 / 角色的导入 / 背景的认识 / 角色的操作 / 声音的导入 / 逻辑推理与编程数学
- L2（4-5 年级·基础）：多角色设置 / 画笔 / 选择语句 / 循环语句 / 移动中的侦测 / 运算 / 声音进阶 / 逻辑推理与编程数学L2
- L3（5-6 年级·进阶）：变量 / 广播消息 / 克隆 / 运算-随机数 / 逻辑推理与编程数学L3
- L4（6 年级+·高级）：列表 / 函数-自制积木 / 条件语句 / 字符串处理 / 逻辑推理与编程数学L4

字段说明（对齐 backend/app/models/question.py）：
- syllabus_version: scratch-l1 ~ scratch-l4
- grade_level: 建议年级
- knowledge_point: 考纲知识点（原名，存储层用）
- q_type: single / judge / coding / program
- content / answer / difficulty(1-5) / explanation
- coding 题: answer 为 → 分隔的积木顺序，blocks_json 由 seed 脚本回填
- program 题: program_lang="scratch", grading_rules 为 JSON 字符串
  grading_rules 格式: [{"check":"opcode_exists","opcodes":["event_whenflagclicked"]}, ...]

文案规范（对齐 AGENTS.md）：
- Scratch 题目面对 2-6 年级小朋友，必须使用口语化、童趣化的语言
- 禁用 session/token/报错/算法/KP 等术语
"""
import json


def _scratch_grading(rules):
    """生成 Scratch 编程题 grading_rules JSON 字符串。

    Args:
        rules: [{"check":"opcode_exists","opcodes":["event_whenflagclicked"]},
                {"check":"opcode_count","opcode":"motion_movesteps","min":1}, ...]
    """
    return json.dumps(rules, ensure_ascii=False)


# =========================================================================
# Scratch L1（27 题）：入门
# 知识点：熟悉编程软件 / 角色的导入 / 背景的认识 / 角色的操作 / 声音的导入 / 逻辑推理与编程数学
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
SCRATCH_L1_QUESTIONS = [
    # =============== L1 · 熟悉编程软件（2 单选 + 1 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 2, "knowledge_point": "熟悉编程软件",
        "q_type": "single",
        "content": "Scratch 软件里，小猫在上面表演的那个大白屏幕叫什么名字？A.舞台 B.积木区 C.角色列表",
        "answer": "A", "difficulty": 1,
        "explanation": "舞台就像剧场里的大幕布，小猫在上面又跳又唱～积木区是拼程序方块的地方，角色列表是管小演员名单的地方，都不是表演的屏幕哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "熟悉编程软件",
        "q_type": "single",
        "content": "想让小猫动起来，要把积木拖到哪里拼起来？A.中间的脚本区（拼积木的地方） B.舞台上面 C.角色列表里",
        "answer": "A", "difficulty": 2,
        "explanation": "积木要拖到中间的脚本区拼成一段程序，小猫才会听话地动起来～舞台只是表演的地方，角色列表是管小动物资料的地方，都不能拼积木！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "熟悉编程软件",
        "q_type": "judge",
        "content": "Scratch 的积木按颜色分类，不同颜色代表不同的功能。",
        "answer": "true", "difficulty": 1,
        "explanation": "对呀！蓝色是运动积木（走路、旋转），紫色是外观积木（换造型、说话），黄色是事件开关……不同颜色不同本领，找积木超方便！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "熟悉编程软件",
        "q_type": "program", "program_lang": "scratch",
        "content": "小猫刚来到 Scratch 世界，想和大家打个招呼。请用积木拼一段程序：点击绿旗启动→小猫说'你好呀'2秒→换成下一个造型→播放声音'喵'。",
        "answer": "see_grading_rules", "difficulty": 2,
        "explanation": "这是一段打招呼小节目！点绿旗启动→喊一声'你好呀'→换个造型摆个 pose→播放一声'喵'，小猫又说话又变样又唱歌，超有戏！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["looks_sayforsecs"], "desc": "必须有说话积木"},
            {"check": "opcode_exists", "opcodes": ["looks_nextcostume"], "desc": "必须有换造型积木"},
            {"check": "opcode_exists", "opcodes": ["sound_play"], "desc": "必须有播放声音积木"},
        ]),
    },

    # =============== L1 · 角色的导入（4 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 2, "knowledge_point": "角色的导入",
        "q_type": "single",
        "content": "想新增一只小狗当角色，应该点哪里？A.右下角角色区的'选择一个角色'加号 B.左上角的'文件'菜单 C.舞台区的背景按钮",
        "answer": "A", "difficulty": 1,
        "explanation": "想请新朋友进来玩，就点右下角'选择一个角色'的加号～文件菜单是存盘的，背景按钮是换舞台背景的，都不请角色哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的导入",
        "q_type": "single",
        "content": "Scratch 自带的'选择一个角色'里有很多角色，它们从哪里来？A.软件自带的角色库 B.你电脑里的照片 C.从网上下载",
        "answer": "A", "difficulty": 1,
        "explanation": "点开'选择一个角色'会跳出一个'角色库'，里面是软件早就准备好的一大堆小动物、人物～不用上网下也不用翻电脑，直接挑就行！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的导入",
        "q_type": "single",
        "content": "小明画了一张熊猫图存在电脑里，想做成 Scratch 角色，应该用哪个功能？A.上传角色 B.选择一个角色（从角色库） C.随机",
        "answer": "A", "difficulty": 2,
        "explanation": "自己画的图在电脑里，得用'上传角色'把它请进来～'选择一个角色'只能挑现成的，'随机'是软件帮你随便挑，都没法用你画的图哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的导入",
        "q_type": "single",
        "content": "想给自己画的角色取个新名字，应该怎么做？A.点角色名字那里直接改 B.只能用原来的名字 C.要重新上传才能改名",
        "answer": "A", "difficulty": 2,
        "explanation": "点一下角色名字那里就能改啦～小猫可以叫'花花'、小狗可以叫'旺财'，想叫啥叫啥！不用重新上传哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 2, "knowledge_point": "角色的导入",
        "q_type": "judge",
        "content": "一个 Scratch 作品里可以同时有很多个角色。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！想加几个加几个，小猫、小狗、太阳、月亮都能一起住进舞台～热闹多了才好玩！",
    },

    # =============== L1 · 背景的认识（3 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "背景的认识",
        "q_type": "single",
        "content": "想给舞台换一张新背景图，应该点哪里？A.右下角'选择一个背景'加号 B.角色区的加号 C.声音标签",
        "answer": "A", "difficulty": 1,
        "explanation": "舞台背景由'舞台'管理，就在右下角'选择一个背景'那个小图标～角色加号是加角色的，声音标签是管声音的，都换不了背景哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "背景的认识",
        "q_type": "single",
        "content": "下面哪个对'背景'的描述是对的？A.背景是舞台后面的图片，角色站在它前面表演 B.背景就是另一个角色 C.背景是声音",
        "answer": "A", "difficulty": 2,
        "explanation": "背景就像舞台后面挂的大画布，小猫小狗这些角色站在画布前面表演～它本身不会动也不会说话，只是一张'风景'哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "背景的认识",
        "q_type": "single",
        "content": "一个舞台可以同时有几张背景？A.可以有很多张，随时切换 B.只能有一张 C.一张也不能有",
        "answer": "A", "difficulty": 2,
        "explanation": "可以放好多张背景哦！比如白天一张、晚上一张，用积木一换就变啦～就像舞台剧换幕布一样，超酷！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "背景的认识",
        "q_type": "judge",
        "content": "背景和角色是一回事，没有区别。",
        "answer": "false", "difficulty": 2,
        "explanation": "不对哦！背景是舞台后面那张不会动的画，角色是会动会说话的小演员～它俩分工不一样，不能搞混啦！",
    },

    # =============== L1 · 角色的操作（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 2, "knowledge_point": "角色的操作",
        "q_type": "single",
        "content": "想让小猫往前走，应该用哪个积木？A.移动10步 B.说你好 C.播放声音",
        "answer": "A", "difficulty": 1,
        "explanation": "'移动 10 步'就是让小猫往前走的指令～'说你好'是冒气泡说话，'播放声音'是出声音，都不让它走路哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的操作",
        "q_type": "single",
        "content": "想让小猫往左扭一点点，应该用哪个积木？A.左转15度 B.右转15度 C.移动10步",
        "answer": "A", "difficulty": 2,
        "explanation": "'左转 15 度'让小猫往左扭头～右转是往右扭，移动是直走不拐弯～分清左右不迷路！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的操作",
        "q_type": "single",
        "content": "想给小猫换一个造型（比如从站着变成坐着），应该用哪个积木？A.换成下一个造型 B.移动10步 C.播放声音",
        "answer": "A", "difficulty": 2,
        "explanation": "'换成下一个造型'就像翻照片，下一张是坐着的姿势～移动是走路，播放声音是出声音，都换不了造型！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的操作",
        "q_type": "judge",
        "content": "小猫可以同时有多个造型，用积木切换造型就像放动画片一样。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！造型就像一叠照片，快速翻就有动画感～小猫走路的动画就是这么做的，超酷！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "角色的操作",
        "q_type": "judge",
        "content": "用'移动10步'积木，小猫只会朝它面向的方向走。",
        "answer": "true", "difficulty": 2,
        "explanation": "对呀！小猫脸朝哪边走哪边～想让往右走，先把它'面向 90 方向'（朝右），再'移动 10 步'就乖乖往右啦！",
    },

    # =============== L1 · 声音的导入（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "声音的导入",
        "q_type": "single",
        "content": "想给小猫加一个'喵'的声音，应该点哪个标签？A.声音标签 B.造型标签 C.代码标签",
        "answer": "A", "difficulty": 1,
        "explanation": "'声音'标签是专门管声音的，点进去就能录音或选声音～造型管外观，代码管积木，都不出声哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "声音的导入",
        "q_type": "single",
        "content": "声音标签里想用 Scratch 自带的声音，应该点哪个按钮？A.选择一个声音 B.上传声音 C.录音",
        "answer": "A", "difficulty": 2,
        "explanation": "'选择一个声音'里有一大堆软件准备好的猫叫、狗叫、咚咚响～'上传'是用你电脑里的声音，'录音'是用麦克风自己录，看你需要哪个！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "声音的导入",
        "q_type": "judge",
        "content": "想用麦克风录下自己说话的声音，可以点'录音'按钮。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！点'录音'按钮，对着麦克风说说话，你的声音就能进 Scratch 啦～想给自己的小猫配音，超简单！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "声音的导入",
        "q_type": "judge",
        "content": "一个角色只能有一个声音。",
        "answer": "false", "difficulty": 2,
        "explanation": "错啦！一个角色可以装好多声音～喵、咕噜、呼呼……想加几个加几个，要用哪个就播哪个！",
    },

    # =============== L1 · 逻辑推理与编程数学（1 单选 + 3 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l1", "grade_level": 2, "knowledge_point": "逻辑推理与编程数学",
        "q_type": "single",
        "content": "小猫从位置 5 走 3 步到位置 8，又退 2 步，现在它在几号位置？A.6 B.8 C.10",
        "answer": "A", "difficulty": 1,
        "explanation": "5 + 3 = 8，再 -2 = 6 呀！往前走是加，往后退是减，跟小朋友排队数数一样～算一算，6 号位置！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "逻辑推理与编程数学",
        "q_type": "judge",
        "content": "想让小猫重复 3 次走 10 步，可以用'重复3次'积木包住'移动10步'。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！把'移动 10 步'塞进'重复 3 次'圈圈里，它就会跑 3 遍，一共走 30 步～比写三次'移动 10 步'省事多啦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "逻辑推理与编程数学",
        "q_type": "judge",
        "content": "积木顺序是：移动10步→说你好→移动10步。小猫一共走了20步。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！一共走两次'移动 10 步'，10 + 10 = 20 步！中间那次'说你好'只是说话没走路，别算进去哦～",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "逻辑推理与编程数学",
        "q_type": "judge",
        "content": "小猫面向 90 方向（朝右），用'移动10步'后会往左走。",
        "answer": "false", "difficulty": 2,
        "explanation": "错啦！90 方向就是朝右，'移动 10 步'会让小猫往右走～想往左走要面向 -90（也就是 270）方向哦！",
    },
    {
        "syllabus_version": "scratch-l1", "grade_level": 3, "knowledge_point": "逻辑推理与编程数学",
        "q_type": "program", "program_lang": "scratch",
        "content": "小猫要从起点出发，走一个正方形回到原点。正方形有 4 条边，每条边走 80 步，每走完一条边右转 90 度。请用积木拼一段程序：点击绿旗启动→重复 4 次（移动 80 步→右转 90 度）。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "走正方形小窍门：4 条边 + 每次转 90 度 = 一圈 360 度正好回原点～用'重复 4 次'包住'移动 80 步'和'右转 90 度'，小猫就走出了方方正正的正方形！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["control_repeat"], "desc": "必须有重复执行积木"},
            {"check": "opcode_count", "opcode": "motion_movesteps", "min": 1, "desc": "必须有移动积木"},
            {"check": "opcode_count", "opcode": "motion_turnright", "min": 1, "desc": "必须有右转积木"},
        ]),
    },
]


# =========================================================================
# Scratch L2（27 题）：基础
# 知识点：多角色设置 / 画笔 / 选择语句 / 循环语句 / 移动中的侦测 / 运算 / 声音进阶 / 逻辑推理与编程数学L2
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
SCRATCH_L2_QUESTIONS = [
    # =============== L2 · 多角色设置（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "多角色设置",
        "q_type": "single",
        "content": "一个 Scratch 作品里有两个角色：小猫和小狗。想让它们同时出现在舞台上不同的位置，应该怎么做？A.分别拖动每个角色到想要的位置 B.只能用一个角色 C.把舞台变大",
        "answer": "A", "difficulty": 2,
        "explanation": "每个角色都可以单独拖到舞台上想要的位置，就像摆玩具一样～小猫放左边，小狗放右边，想怎么摆怎么摆！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "多角色设置",
        "q_type": "single",
        "content": "舞台上有小猫和小狗两个角色，想让小狗永远跟着小猫走，应该用？A.重复执行积木里放'移到小猫' B.只放一次'移到小猫' C.让小狗自己'移动10步'",
        "answer": "A", "difficulty": 3,
        "explanation": "小猫会动，所以小狗得'一直跟着'，用'重复执行'包住'移到小猫'才行～只放一次就跟一下，小猫跑远了就跟丢啦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "多角色设置",
        "q_type": "judge",
        "content": "不同角色可以有自己的脚本，互不干扰。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！每个角色都像独立的小朋友，自己的积木自己做，互不打架～点哪个角色就编辑哪个角色的脚本。",
    },

    # =============== L2 · 画笔（2 单选 + 1 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "画笔",
        "q_type": "single",
        "content": "想让小猫走过的地方留下彩色脚印，应该先用哪个积木？A.落笔 B.抬笔 C.移动10步",
        "answer": "A", "difficulty": 2,
        "explanation": "'落笔'就像把笔尖按到纸上，之后走路才会留痕迹～'抬笔'是抬起来不画了，'移动'只是走路不决定画不画哦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "画笔",
        "q_type": "single",
        "content": "画完一个图形后想换个地方画新的，应该先怎么做？A.抬笔再移动 B.直接移动 C.清空画面",
        "answer": "A", "difficulty": 2,
        "explanation": "画完想换地方画新的，先'抬笔'再走过去，到位置了再'落笔'～不然路上会画一堆乱线哦！直接移动会拖着笔画，清空就把画好的也擦掉了！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "画笔",
        "q_type": "judge",
        "content": "画完一个图形后，应该用'抬笔'积木把笔抬起来，移动到新位置才不会乱画。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！画完一个图想换个地方画新的，先'抬笔'再走过去，到位置了再'落笔'～不然路上会画一堆乱线哦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "画笔",
        "q_type": "program", "program_lang": "scratch",
        "content": "小猫要用画笔画一个正方形。请用积木拼一段程序：点击绿旗启动→清空画面→抬笔→移到(0,0)→落笔→重复 4 次（移动 80 步→右转 90 度）。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "画正方形步骤：先清空旧画→抬笔走到中心(0,0)→落笔开始画→重复 4 次：走 80 步+右转 90 度～4 条边围成一个正方形，加上画笔颜色还能变彩的！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["pen_clear"], "desc": "必须有清空画面积木"},
            {"check": "opcode_exists", "opcodes": ["pen_penDown"], "desc": "必须有落笔积木"},
            {"check": "opcode_exists", "opcodes": ["control_repeat"], "desc": "必须有重复执行积木"},
        ]),
    },

    # =============== L2 · 选择语句（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "选择语句",
        "q_type": "single",
        "content": "判断'分数是否等于 10'，要用哪个积木？A.'='比较运算符 B.'+'加法 C.连接文字",
        "answer": "A", "difficulty": 2,
        "explanation": "想比一比是不是相等，用'='这个比较运算符～'+'是加法算数，'连接'是拼文字，都判不了真假哦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "选择语句",
        "q_type": "single",
        "content": "做'碰到障碍就说哎呀'的效果，应该用哪个积木？A.如果 那么 B.重复执行 C.移动10步",
        "answer": "A", "difficulty": 3,
        "explanation": "'如果碰到障碍，那么说哎呀'——典型的'如果…那么…'！碰到才说，没碰到就不说～重复是循环，移动是走路，都不判断！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "选择语句",
        "q_type": "judge",
        "content": "'如果 那么'积木里，条件成立时才会执行里面的积木。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！条件是真才放行（做里面的事），是假就跳过～就像门卫：你说对了口令才让你进！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "选择语句",
        "q_type": "judge",
        "content": "'如果 那么 否则'积木只能做一件事，不能处理两种情况。",
        "answer": "false", "difficulty": 3,
        "explanation": "错啦！'如果…那么…否则'能处理两种：条件成立做'那么'那部分，不成立做'否则'那部分～比如'下雨就带伞，否则带太阳帽'！",
    },

    # =============== L2 · 循环语句（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "循环语句",
        "q_type": "single",
        "content": "想让小猫重复 10 次走 10 步，应该用哪个积木？A.重复10次 B.重复执行 C.如果 那么",
        "answer": "A", "difficulty": 2,
        "explanation": "'重复 10 次'就是固定跑 10 遍～'重复执行'是永远不停（除非用别的积木让它停），'如果那么'是判断不是循环！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "循环语句",
        "q_type": "single",
        "content": "想让小猫一直走，直到碰到边缘才停，用哪个积木最合适？A.重复执行直到 碰到边缘 B.重复10次 C.等待1秒",
        "answer": "A", "difficulty": 3,
        "explanation": "'重复执行直到…'就是'一直做到某件事发生才停'～这里就是'一直走到碰到边缘'～重复 10 次到不了边缘就停了，等待根本不走，都不行！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "循环语句",
        "q_type": "judge",
        "content": "'重复执行'积木里的脚本会一直跑，不会自己停。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！'重复执行'就是永远循环，除非用'停止全部'或者程序被关掉，不然一直转圈圈～想做'一直巡逻'就用它！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "循环语句",
        "q_type": "judge",
        "content": "'重复5次'和'重复执行'是一样的，都不会停。",
        "answer": "false", "difficulty": 3,
        "explanation": "不一样哦！'重复 5 次'跑 5 遍就停，'重复执行'是永远不停～想'跳 5 下'用前者，想'一直跳'用后者！",
    },

    # =============== L2 · 移动中的侦测（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "移动中的侦测",
        "q_type": "single",
        "content": "想知道小猫有没有碰到小狗，应该用哪个积木？A.碰到 小狗 B.移动10步 C.说你好",
        "answer": "A", "difficulty": 2,
        "explanation": "'碰到 小狗？'这块侦测积木能告诉你小猫有没有撞上小狗～它返回真/假，正好给'如果那么'用！移动是走路，说话不判断！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "移动中的侦测",
        "q_type": "single",
        "content": "做'碰到红色墙壁就反弹'的游戏，要用什么积木来判断颜色？A.碰到颜色 红 B.碰到 小狗 C.说 红色",
        "answer": "A", "difficulty": 3,
        "explanation": "'碰到颜色 红？'能检测小猫有没有撞上红色的东西～'碰到角色'只查角色不查颜色，'说'只是冒气泡，都不查颜色！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "移动中的侦测",
        "q_type": "judge",
        "content": "'碰到鼠标指针'可以判断角色是不是碰到了鼠标。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！这块侦测积木检测角色和鼠标指针有没有碰到一起～做'用鼠标赶小猫'的游戏就靠它啦！",
    },

    # =============== L2 · 运算（2 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "运算",
        "q_type": "single",
        "content": "想算 5 加 3 等于几，应该用哪个积木？A.'+'加法运算 B.'='比较运算 C.连接文字",
        "answer": "A", "difficulty": 2,
        "explanation": "加法用'+'运算积木～'='是比相等，'连接'是拼文字，都不是算数的料！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "运算",
        "q_type": "single",
        "content": "想算 10 除以 2 等于几，用哪个运算积木？A.'/'除法 B.'*'乘法 C.'+'加法",
        "answer": "A", "difficulty": 3,
        "explanation": "除法用'/'～10 / 2 = 5，就是分成 2 份每份 5 个～'*'是乘法（10×2=20），'+'是加法（10+2=12），都不一样哦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "运算",
        "q_type": "judge",
        "content": "'连接 苹果 和 香蕉'积木的结果是'苹果香蕉'。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！'连接'积木把两段文字拼起来，苹果+香蕉='苹果香蕉'～做计分牌拼名字+分数就靠它！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "运算",
        "q_type": "judge",
        "content": "'4 > 3'的结果是 false（假）。",
        "answer": "false", "difficulty": 3,
        "explanation": "错啦！4 比 3 大，所以'4 > 3'是真的（true）～'>'就是'大于'的意思，左边比右边大就是真！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "运算",
        "q_type": "program", "program_lang": "scratch",
        "content": "小猫要表演算术魔术。请用积木拼一段程序：点击绿旗启动→小猫说'看我算得快'2秒→把 8 和 5 加起来→把计算结果说出来。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "算术魔术秀！点绿旗启动→先说'看我算得快'热热身→用'+'把 8 和 5 加起来（等于 13）→把结果说出来～运算积木加说话积木一起用，小猫秒变数学小能手！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["looks_sayforsecs"], "desc": "必须有说话2秒积木"},
            {"check": "opcode_exists", "opcodes": ["operator_add"], "desc": "必须有加法运算积木"},
            {"check": "opcode_exists", "opcodes": ["looks_say"], "desc": "必须有说出结果积木"},
        ]),
    },

    # =============== L2 · 声音进阶（1 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "声音进阶",
        "q_type": "single",
        "content": "想让声音变尖一点（像小鸟叫），应该用哪个积木？A.将音调设为 80 B.将音量设为 80 C.将节奏设为 120",
        "answer": "A", "difficulty": 2,
        "explanation": "音调管'尖不尖'～设高就变尖嗓门像小鸟，设低就变粗嗓门像大熊～音量管大小声，节奏管快慢，三个不一样哦！",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "声音进阶",
        "q_type": "judge",
        "content": "播放声音之前，可以用'将音量设为'积木调声音大小。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！'将音量设为 0'就静音，'100'就最大声～想悄悄说话设小一点，想大喊大叫设大一点，超灵活！",
    },

    # =============== L2 · 逻辑推理与编程数学L2（2 单选） ===============
    {
        "syllabus_version": "scratch-l2", "grade_level": 4, "knowledge_point": "逻辑推理与编程数学L2",
        "q_type": "single",
        "content": "小猫在 x=0，重复 3 次'移动 50 步'，最后一次走完在哪个 x？A.150 B.50 C.100",
        "answer": "A", "difficulty": 2,
        "explanation": "每次 50 步，3 次就是 50×3 = 150！小猫从 0 走到 150，重复乘法比加法快多啦～",
    },
    {
        "syllabus_version": "scratch-l2", "grade_level": 5, "knowledge_point": "逻辑推理与编程数学L2",
        "q_type": "single",
        "content": "小猫重复 4 次走 10 步、右转 90 度，画出来是什么图形？A.正方形 B.三角形 C.圆形",
        "answer": "A", "difficulty": 3,
        "explanation": "4 次 + 每次转 90 度 = 一圈 360 度，正好回到起点，画出 4 条边一样长的正方形～三角形是 3 次 120 度，圆形要超多次小角度！",
    },
]


# =========================================================================
# Scratch L3（27 题）：进阶
# 知识点：变量 / 广播消息 / 克隆 / 运算-随机数 / 逻辑推理与编程数学L3
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
SCRATCH_L3_QUESTIONS = [
    # =============== L3 · 变量（4 单选 + 3 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l3", "grade_level": 4, "knowledge_point": "变量",
        "q_type": "single",
        "content": "变量的作用是？A.存储数据 B.连接两段文字 C.比较两个数字大小",
        "answer": "A", "difficulty": 2,
        "explanation": "变量就是'给数字或文字起个名字放起来'，随时可以拿出来看或者改！连接文字是运算模块的'字符串连接'，比大小是'比较运算符'——都不是存东西的活儿～",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 4, "knowledge_point": "变量",
        "q_type": "single",
        "content": "「将 分数 增加 1」让分数变成？A.加 1 B.减 1 C.清零",
        "answer": "A", "difficulty": 2,
        "explanation": "就是加一分呀！比如原来 5 分，用这块积木后就变 6 分。想减分写 -1 就行，想清零得用另一块「将 分数 设为 0」～",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "变量",
        "q_type": "single",
        "content": "新建变量时，'适用于所有角色'和'仅适用于当前角色'的区别是？A.前者所有角色都能看到和改，后者只有当前角色能用 B.前者只能读不能改 C.后者速度更快 D.没区别",
        "answer": "A", "difficulty": 3,
        "explanation": "全局变量（适用于所有角色）就像班级公告栏，所有角色都能看能改；局部变量（仅适用于当前角色）像私人日记本，只有自己能看～做计分牌用全局，做各自技能用局部！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "变量",
        "q_type": "single",
        "content": "做点击计数游戏，变量'次数'初始该设为多少？A.0 B.1 C.10 D.随便设",
        "answer": "A", "difficulty": 2,
        "explanation": "计数要从 0 开始，每点一次加 1～如果从 1 开始就多算了一次，从 10 开始就乱套啦！'归零'就是设为 0 的意思。",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 4, "knowledge_point": "变量",
        "q_type": "judge",
        "content": "同一个变量在不同角色里可以取不同的值（限「仅适用于当前角色」）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！新建变量时如果勾'只给我用'，每个角色就都有一份独立的'分数'，你踢你的球我做我的题，各不打扰～",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "变量",
        "q_type": "judge",
        "content": "变量里只能存数字，不能存文字。",
        "answer": "false", "difficulty": 2,
        "explanation": "错啦！变量既能存数字（5、100），也能存文字（'你好'、'小猫'）～还能存算式的结果，超灵活！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "变量",
        "q_type": "judge",
        "content": "「将 分数 设为 0」和「将 分数 增加 0」效果一样。",
        "answer": "false", "difficulty": 3,
        "explanation": "不一样！'设为 0'是把分数强制变成 0（不管原来是几）；'增加 0'是加 0，分数不变～设为是覆盖，增加是累加！",
    },

    # =============== L3 · 广播消息（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "single",
        "content": "让两个角色配合动作，最方便的是？A.广播 B.移到对方位置告诉它 C.用「说」显示消息",
        "answer": "A", "difficulty": 2,
        "explanation": "广播就像喊喇叭：一个角色喊一声「开始」，其他角色听见就动起来～「跑过去告诉」太笨了，「说话」其他角色又「看不到」，还是广播最直接！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "single",
        "content": "小猫吃到鱼后，想让另一个角色小狗跳起来庆祝，最合适的做法是？A.小猫「广播 吃到鱼」，小狗「当接收到 吃到鱼」就跳 B.小猫「说 吃到鱼了」，指望小狗自己看见 C.让小猫「移到小狗位置」告诉它 D.小猫和小狗都放「重复执行 → 等待」互相等",
        "answer": "A", "difficulty": 3,
        "explanation": "角色之间悄悄传消息最好用广播！小猫喊一声「吃到鱼」，小狗听到就跳～「说」其他角色其实听不到，「跑过去」多此一举，「重复等待」又卡又浪费！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "single",
        "content": "「广播」和「广播并等待」的区别是？A.前者发完就继续，后者等所有接收者处理完才继续 B.前者更快 C.后者不能发消息 D.没区别",
        "answer": "A", "difficulty": 3,
        "explanation": "「广播」像发传单，发完就走；「广播并等待」像打电话，等对方说完才挂～要做「小猫说完话再让小狗跳」就用后者，要同时进行就用前者！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "judge",
        "content": "一个广播消息可以同时被多个角色接收，它们都会执行自己的「当接收到」脚本。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！广播像大喇叭喊一声，所有装了「当接收到这条消息」的角色都会同时动起来～做「烟花」就靠它，一个广播让好多烟花一起炸！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "judge",
        "content": "广播消息的名字可以随便取，但建议取有意义的名字（如「游戏开始」「得分」）方便看懂。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！消息名就像口令，取'开始'、'得分'这种看得懂的名字，自己和别人都能明白～取'消息1'、'aaa'这种名字回头就忘了是干啥的！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "广播消息",
        "q_type": "program", "program_lang": "scratch",
        "content": "做一个小剧场：点击绿旗→小猫说「我开演啦」1秒→小猫广播「开始跳舞」→小狗收到「开始跳舞」后说「收到」1秒并换下一个造型。请用积木拼出小猫的脚本。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "小猫的脚本：绿旗→说「我开演啦」1秒→广播「开始跳舞」～小狗另写一段：当接收到「开始跳舞」→说「收到」1秒→换下一个造型。广播让两个角色配合得天衣无缝！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["looks_sayforsecs"], "desc": "必须有说话积木"},
            {"check": "opcode_exists", "opcodes": ["event_broadcast"], "desc": "必须有广播积木"},
        ]),
    },

    # =============== L3 · 克隆（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "克隆",
        "q_type": "single",
        "content": "「克隆自己」积木的作用是？A.复制一个和自己一模一样的克隆体 B.删除自己 C.换造型 D.移动",
        "answer": "A", "difficulty": 2,
        "explanation": "「克隆自己」就像按下复印机按钮，每按一次就多一个自己～克隆体跟本体长得一样，位置也一样，可以单独写脚本控制！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "克隆",
        "q_type": "single",
        "content": "做一个「下雨」效果，让雨滴不断从天上落下来，最合适的思路是？A.循环里反复「克隆自己」，克隆体启动时从随机 x 位置落下 B.提前复制 100 个雨滴角色手动摆放 C.用「移动积木」让一个角色走 Z 字形 D.用「说」显示「雨」这个字",
        "answer": "A", "difficulty": 3,
        "explanation": "雨滴那么多手动摆 100 个角色累死人！用循环让一个雨滴角色不停「克隆自己」，每个克隆体从天上随机位置往下掉——就是真下雨啦，又快又轻松！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "克隆",
        "q_type": "single",
        "content": "克隆体太多卡住了，应该用哪块积木清理？A.删除此克隆体 B.清空画面 C.停止全部 D.隐藏",
        "answer": "A", "difficulty": 3,
        "explanation": "克隆体用完要「删除此克隆体」～像雨滴落到地面就该消失，不然越积越多电脑会卡！清空画面只擦画不删克隆体，停止全部会停整个程序，隐藏只是看不见还在。",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "克隆",
        "q_type": "judge",
        "content": "克隆体诞生时，会执行「当作为克隆体启动时」积木下面的脚本。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！每个克隆体一出生就开始跑「当作为克隆体启动时」下面的积木～本体写一次，所有克隆体都照着做，这就是克隆的威力！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "克隆",
        "q_type": "judge",
        "content": "本体和克隆体共享同一段脚本，不能分别控制。",
        "answer": "false", "difficulty": 3,
        "explanation": "错！本体有自己的脚本（如绿旗启动），克隆体有「当作为克隆体启动时」的脚本～它们各跑各的，可以分别控制位置、造型、动作！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "克隆",
        "q_type": "program", "program_lang": "scratch",
        "content": "做烟花效果：点击绿旗→重复执行（克隆自己→等待 0.5 秒）；克隆体启动时移到随机位置→显示→等待 1 秒→删除此克隆体。请用积木拼出本体的脚本。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "本体脚本：绿旗→重复执行（克隆自己+等待 0.5 秒），每隔半秒生一个克隆体～克隆体脚本另写：当作为克隆体启动时→移到随机位置→显示→等待 1 秒→删除。烟花不停炸！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["control_repeat"], "desc": "必须有重复执行积木"},
            {"check": "opcode_exists", "opcodes": ["control_create_clone_of"], "desc": "必须有克隆积木"},
            {"check": "opcode_exists", "opcodes": ["control_wait"], "desc": "必须有等待积木"},
        ]),
    },

    # =============== L3 · 运算-随机数（3 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "运算-随机数",
        "q_type": "single",
        "content": "「在1到10之间随机取数」最小可能取到？A.0 B.1 C.10",
        "answer": "B", "difficulty": 2,
        "explanation": "从 1 到 10 都算数哦（包括两头 1 和 10）！所以最小是 1，最大是 10，不会跑到 0 或 11 去～骰子游戏、抽奖游戏最爱用它啦！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "运算-随机数",
        "q_type": "single",
        "content": "想让掷骰子游戏每次显示 1 到 6 中的一个数，下面哪个写法是对的？A.在1到6之间取随机数 B.在0到6之间取随机数 C.在1到7之间取随机数 D.在6到1之间取随机数",
        "answer": "A", "difficulty": 3,
        "explanation": "骰子只有 1、2、3、4、5、6 六个面～A 刚好从 1 到 6 都算；B 可能出 0（骰子没 0 点），C 可能出 7（也没 7 点），D 顺序倒着写虽然能跑但不规范啦！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "运算-随机数",
        "q_type": "single",
        "content": "想让小猫每次出现在舞台随机位置，x 坐标该用什么？A.在 -240 到 240 之间取随机数 B.固定写 100 C.写 0 D.用「移动 10 步」",
        "answer": "A", "difficulty": 3,
        "explanation": "舞台 x 范围是 -240 到 240，用随机数每次出现在不同位置～固定写 100 就每次都在同一地方，写 0 更是死板，移动是走路不是定位！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "运算-随机数",
        "q_type": "judge",
        "content": "「在 1 到 1 之间取随机数」结果永远是 1。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！最大和最小都是 1，那取出来当然只能是 1～这种「随机」其实不随机，但在某些固定场景（如必须取某值）会用上。",
    },

    # =============== L3 · 逻辑推理与编程数学L3（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "逻辑推理与编程数学L3",
        "q_type": "single",
        "content": "小猫有 3 条命，被怪物碰到减 1 条，碰到 2 次后还剩几条？A.1 B.2 C.3 D.0",
        "answer": "A", "difficulty": 2,
        "explanation": "3 - 1 - 1 = 1！这就是变量减法～用「将 生命 减少 1」积木，每碰一次减一条，碰两次就剩 1 条命啦！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "逻辑推理与编程数学L3",
        "q_type": "single",
        "content": "「如果 生命 = 0 那么」广播「游戏结束」，这块积木什么时候触发？A.生命减到 0 时 B.游戏一开始 C.永远不触发 D.生命等于任意数时",
        "answer": "A", "difficulty": 3,
        "explanation": "条件是「生命 = 0」，只有生命真的变成 0 才成立～这时才广播「游戏结束」，其他情况（如生命=3）都不触发。这就是用变量做游戏结束判断！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 5, "knowledge_point": "逻辑推理与编程数学L3",
        "q_type": "judge",
        "content": "做计分游戏时，得分变量应该用「将 得分 增加 1」而不是「将 得分 设为 1」。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！「增加 1」是在原分上加 1（5→6→7…）；「设为 1」是覆盖成 1（5→1），分数永远卡在 1～计分要用「增加」！",
    },
    {
        "syllabus_version": "scratch-l3", "grade_level": 6, "knowledge_point": "逻辑推理与编程数学L3",
        "q_type": "judge",
        "content": "变量可以同时存多个数字，像一个书包。",
        "answer": "false", "difficulty": 3,
        "explanation": "错啦！变量一次只能存一个值（一个数字或一段文字）～想存多个要用「列表」（L4 会学）。变量像小盒子，列表才像大书包！",
    },
]


# =========================================================================
# Scratch L4（27 题）：高级
# 知识点：列表 / 函数-自制积木 / 条件语句 / 字符串处理 / 逻辑推理与编程数学L4
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
SCRATCH_L4_QUESTIONS = [
    # =============== L4 · 列表（4 单选 + 3 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "single",
        "content": "想保存 30 个同学的分数，用什么最合适？A.变量 B.列表 C.广播",
        "answer": "B", "difficulty": 3,
        "explanation": "30 个分数用变量得开 30 个盒子太挤啦！列表就像一个大书包能装很多，还能按顺序编号（第 1 个、第 2 个……）；广播只是发消息，不是存东西哦～",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "single",
        "content": "列表里第 3 个数据怎么取出来？A.「列表 的第 3 项」积木 B.「列表 的第 1 项」 C.「变量 增加 3」 D.「连接 列表 和 3」",
        "answer": "A", "difficulty": 3,
        "explanation": "列表按编号取数据，用「第 3 项」积木～第 1 项是开头那个，第 3 项才是第三个。变量是存一个数，连接是拼文字，都取不了列表里的东西！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "single",
        "content": "想往列表最后添加一个新数据，用哪块积木？A.「将 … 添加到 列表」 B.「将 列表 设为 …」 C.「删除 列表 的第 1 项」 D.「插入 … 到 列表 的第 1 项」",
        "answer": "A", "difficulty": 3,
        "explanation": "「添加」是在列表末尾加一个新数据，像排队站最后～「设为」是覆盖整个列表，「删除」是去掉，「插入」是塞到中间。加在最后用「添加」！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "single",
        "content": "「列表的长度」积木返回什么？A.列表里有几个数据 B.列表第一项的值 C.列表的编号 D.列表的名字",
        "answer": "A", "difficulty": 3,
        "explanation": "「长度」就是列表里装了多少个数据～比如有 30 个分数，长度就是 30。想知道列表有多少项，用它就对了！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "judge",
        "content": "列表和变量最大的区别是：列表能一次装很多个数据，变量只能装一个。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！变量就像一个小盒子只放一样东西，列表像一个书包能塞好多本书～存 30 个分数、10 个名字、100 条日志，通通交给列表最省心！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "judge",
        "content": "列表里数据的编号从 0 开始（第 0 项、第 1 项……）。",
        "answer": "false", "difficulty": 3,
        "explanation": "错！Scratch 列表编号从 1 开始（第 1 项、第 2 项……）～这跟有些编程语言（从 0 开始）不一样，别搞混啦！第 1 项就是第一个数据。",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "judge",
        "content": "可以用「重复执行」+「计数器变量」遍历（一个个看）列表里的所有数据。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！设个变量 i 从 1 开始，重复「列表长度」次，每次取「第 i 项」再「将 i 增加 1」～就能挨个看完所有数据，这是列表的常用招数！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "列表",
        "q_type": "program", "program_lang": "scratch",
        "content": "做一个购物清单：点击绿旗→清空「清单」列表→重复 3 次（询问「要买什么」并等待回答→将回答添加到「清单」）→说「清单记好啦」。请用积木拼出脚本。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "绿旗→清空列表（重新开始记）→重复 3 次：问「要买什么」+把回答加进列表→最后说「清单记好啦」～询问+添加+循环，购物清单 App 的核心套路！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["control_repeat"], "desc": "必须有重复执行积木"},
            {"check": "opcode_exists", "opcodes": ["sensing_askandwait"], "desc": "必须有询问积木"},
            {"check": "opcode_exists", "opcodes": ["data_addtolist"], "desc": "必须有添加到列表积木"},
        ]),
    },

    # =============== L4 · 函数-自制积木（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "single",
        "content": "自制积木的好处是什么？A.把重复的积木打包成一块，用的时候直接调用 B.让程序变长 C.代替所有积木 D.让小猫跑得更快",
        "answer": "A", "difficulty": 3,
        "explanation": "自制积木就像「我的专属技能」，把一堆重复的动作打包成一块新积木，之后想用就叫一下，比一直复制粘贴清爽多啦～",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "single",
        "content": "自制积木和「广播消息」都能让代码更整洁，它俩最本质的区别是？A.自制积木像「叫朋友帮忙」，你要等他做完才继续；广播像「发朋友圈」，发完你就走开做别的 B.自制积木只能在一个角色里用，广播能跨角色 C.自制积木必须要输入参数，广播不能带参数 D.广播消息比自制积木更快",
        "answer": "A", "difficulty": 4,
        "explanation": "自制积木就像叫朋友帮忙，你得在门口等他做完再继续；广播像发朋友圈，发完你就走开做别的事啦～这个「等不等」是它俩最大的差别！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "single",
        "content": "自制积木可以带「参数」（输入），参数的作用是？A.让同一块积木根据不同输入做不同事 B.让积木变漂亮 C.代替变量 D.必须有参数才能用",
        "answer": "A", "difficulty": 4,
        "explanation": "参数就像给积木「喂不同的料」～做一块「画正方形 边长」积木，喂 80 画大正方形，喂 40 画小的，一块积木搞定多种情况，超灵活！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "judge",
        "content": "自制积木可以让重复的代码变得更整洁。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！自制积木就像「我的专属技能」，把一堆重复的动作打包成一块新积木，之后想用就叫一下，比一直复制粘贴清爽多啦～",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "judge",
        "content": "自制积木定义好后，可以在任何角色里直接使用（不用再定义）。",
        "answer": "false", "difficulty": 4,
        "explanation": "错！自制积木是「哪个角色定义的，只有那个角色能用」～别的角色想用得自己再定义一遍，或者用广播跨角色调用。自制积木不跨角色！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "函数-自制积木",
        "q_type": "program", "program_lang": "scratch",
        "content": "定义一块自制积木「画正方形 边长」，功能是：落笔→重复 4 次（移动「边长」步→右转 90 度）→抬笔。然后在绿旗点击时调用它画边长 100 的正方形。请用积木拼出调用部分。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "先定义自制积木「画正方形 边长」（里面用参数「边长」代替具体数字）→绿旗点击时调用「画正方形 100」～一块积木画任意大小正方形，参数的威力！",
        "grading_rules": _scratch_grading([
            {"check": "opcode_exists", "opcodes": ["event_whenflagclicked"], "desc": "必须有点击绿旗积木"},
            {"check": "opcode_exists", "opcodes": ["procedures_call"], "desc": "必须有调用自制积木"},
            {"check": "opcode_exists", "opcodes": ["pen_penDown"], "desc": "必须有落笔积木"},
            {"check": "opcode_exists", "opcodes": ["control_repeat"], "desc": "必须有重复执行积木"},
        ]),
    },

    # =============== L4 · 条件语句（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "scratch-l4", "grade_level": 5, "knowledge_point": "条件语句",
        "q_type": "single",
        "content": "在游戏中判断「分数是否≥10」，需要什么积木？A.比较运算符（>、<、=） B.加减乘除运算 C.字符串连接",
        "answer": "A", "difficulty": 3,
        "explanation": "要比大小得用「比较运算符」（>、< 或 =）搭一个「分数 ≥ 10」的判断条件～加减乘除是算数不是判断，字符串连接是拼文字，都产生不了「真/假」哦！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "条件语句",
        "q_type": "single",
        "content": "做「分数≥60显示及格，否则显示不及格」，用哪块积木？A.如果 那么 否则 B.如果 那么 C.重复执行 D.等待",
        "answer": "A", "difficulty": 3,
        "explanation": "有两种情况（及格/不及格）要用「如果…那么…否则」～条件真做「那么」（显示及格），条件假做「否则」（显示不及格），一块积木搞定两种结果！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "条件语句",
        "q_type": "single",
        "content": "「如果 那么 否则」里还能再嵌一个「如果 那么 否则」吗？A.可以，这叫嵌套判断 B.不行，只能用一层 C.会报错 D.只有广播能嵌套",
        "answer": "A", "difficulty": 4,
        "explanation": "可以！这叫「嵌套」～比如「如果分数≥90 那么优秀，否则如果≥60 那么及格，否则不及格」——一层套一层，能处理多种情况！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 5, "knowledge_point": "条件语句",
        "q_type": "judge",
        "content": "「如果那么」积木只有条件成立时才执行内部积木。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！「如果」就像门卫大叔，条件是真才放行（做里面的事），条件是假就关门（跳过）～想「真才做、假不做」就用它！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "条件语句",
        "q_type": "judge",
        "content": "「如果 那么 否则」无论条件真假，都会执行其中一段积木。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！条件真做「那么」，条件假做「否则」～两段必跑其一，不会两段都跑也不会都不跑。这是它和「如果那么」（假就跳过）的区别！",
    },

    # =============== L4 · 字符串处理（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "字符串处理",
        "q_type": "single",
        "content": "想算「Hello」这个词有几个字母，用哪块积木？A.「Hello 的长度」 B.「连接 Hello 和 1」 C.「Hello 的第 1 个字符」 D.「Hello 包含 1 ？」",
        "answer": "A", "difficulty": 3,
        "explanation": "「长度」积木数文字有几个字符～「Hello」有 5 个字母，长度就是 5。连接是拼文字，第 1 个字符是取一个，包含是判断有没有，都数不出长度！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "字符串处理",
        "q_type": "single",
        "content": "「Apple 的第 1 个字符」积木返回什么？A.A B.p C.e D.Apple",
        "answer": "A", "difficulty": 3,
        "explanation": "第 1 个字符就是开头的字母～「Apple」开头是 A，所以返回 A。第 2 个才是 p，第 3 个是 p……从 1 开始数！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "字符串处理",
        "q_type": "single",
        "content": "想判断「回答」里有没有「好」这个字，用哪块积木？A.「回答 包含 好 ？」 B.「回答 的长度」 C.「回答 的第 1 个字符」 D.「连接 回答 和 好」",
        "answer": "A", "difficulty": 3,
        "explanation": "「包含」积木判断一段文字里有没有某个字/词～有就返回 true，没有返回 false。长度是数字数，第 1 个字符是取开头，连接是拼文字，都判断不了！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "字符串处理",
        "q_type": "judge",
        "content": "「连接 Apple 和 Banana」的结果是「AppleBanana」（中间没空格）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！「连接」就是把两段文字首尾拼起来，不会自动加空格～想要「Apple Banana」得连接三个：Apple+空格+Banana。",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "字符串处理",
        "q_type": "judge",
        "content": "一个汉字（如「猫」）的长度是 1。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！Scratch 里一个汉字算 1 个字符～「小猫」长度是 2，「喵喵喵」长度是 3。跟字母一样数，一个字一个长度。",
    },

    # =============== L4 · 逻辑推理与编程数学L4（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "逻辑推理与编程数学L4",
        "q_type": "single",
        "content": "列表「分数」有 5 个数据：80、90、70、100、60。想算总分，思路是？A.设「总分」=0，重复 5 次（将「总分」增加「分数的第 i 项」） B.设「总分」=5 C.用「连接」拼起来 D.用「随机数」",
        "answer": "A", "difficulty": 4,
        "explanation": "算总分要累加：先总分清零，再用循环把每个分数加进去～重复 5 次（因为有 5 个），每次取「第 i 项」加到总分。这是列表+循环的经典组合！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "逻辑推理与编程数学L4",
        "q_type": "single",
        "content": "接上题，总分算出来后求平均分怎么算？A.总分 / 5（列表长度） B.总分 * 5 C.总分 - 5 D.总分 + 5",
        "answer": "A", "difficulty": 4,
        "explanation": "平均分 = 总分 ÷ 个数～5 个分数的总和除以 5 就是平均分。用「列表的长度」代替写死的 5 更通用，列表有几个数据就除以几！",
    },
    {
        "syllabus_version": "scratch-l4", "grade_level": 6, "knowledge_point": "逻辑推理与编程数学L4",
        "q_type": "judge",
        "content": "找列表里最大值的思路：设「最大」=第 1 项，重复遍历，遇到比「最大」大的就更新「最大」。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！这是「打擂台」算法～先让第 1 个当擂主（最大），后面的挨个跟擂主打，打得过（更大）就换人当擂主。遍历完，擂主就是最大值！",
    },
]


# =========================================================================
# 汇总：所有 Scratch 题目（4 级 × 27 题 = 108 题）
# =========================================================================
ALL_SCRATCH_QUESTIONS = (
    SCRATCH_L1_QUESTIONS
    + SCRATCH_L2_QUESTIONS
    + SCRATCH_L3_QUESTIONS
    + SCRATCH_L4_QUESTIONS
)


# =========================================================================
# 各级题目列表映射（方便按级别取用）
# =========================================================================
SCRATCH_QUESTIONS_BY_LEVEL = {
    "scratch-l1": SCRATCH_L1_QUESTIONS,
    "scratch-l2": SCRATCH_L2_QUESTIONS,
    "scratch-l3": SCRATCH_L3_QUESTIONS,
    "scratch-l4": SCRATCH_L4_QUESTIONS,
}


def _verify():
    """自检：题目总数、各级数量、题型分布。"""
    total = len(ALL_SCRATCH_QUESTIONS)
    print(f"总题数: {total}（应为 108）")
    assert total == 108, f"题目总数不对: {total} != 108"

    from collections import Counter

    by_level = Counter(q["syllabus_version"] for q in ALL_SCRATCH_QUESTIONS)
    print("\n各级题数:")
    for lv in range(1, 5):
        key = f"scratch-l{lv}"
        cnt = by_level[key]
        print(f"  {key}: {cnt} 题（应为 27）")
        assert cnt == 27, f"{key} 题数不对: {cnt} != 27"

    print("\n各级题型分布:")
    for lv in range(1, 5):
        key = f"scratch-l{lv}"
        qs = SCRATCH_QUESTIONS_BY_LEVEL[key]
        dist = Counter(q["q_type"] for q in qs)
        print(
            f"  {key}: 单选 {dist['single']} + 判断 {dist['judge']} "
            f"+ 编程 {dist.get('program', 0) + dist.get('coding', 0)} = {sum(dist.values())}"
        )

    print("\n[verify] 全部检查通过 ✓")


if __name__ == "__main__":
    _verify()
