"""Python L1-L6 题库数据（按电子学会青少年软件编程（Python）等级考试标准 2026 修订版）。

共 6 级 × 27 题 = 162 题
每级题型分布：15 单选(single) + 10 判断(judge) + 2 编程(program)

考纲对齐（电子学会青少年软件编程（Python）等级考试标准 2026 修订版）：
- L1（3-6 年级·普及）：简单数学运算与Turtle库（熟悉编程环境，顺序结构）
- L2（4-6 年级·基础）：核心数据类型：列表、元组、字符串、字典（顺序/分支/循环结构）
- L3（6-7 年级·算法入门）：算法：解析、枚举、排序、查找（组合数据类型）
- L4（7-8 年级·进阶）：函数、文件、异常处理（模块化编程）
- L5（8-9 年级·高级）：高级语法与标准库（列表推导式、生成器、切片、解包、math/random/time）
- L6（9 年级+·综合）：数据库操作、面向对象（SQLite、类与对象）

字段说明（对齐 backend/app/models/question.py）：
- syllabus_version: python-l1 ~ python-l6
- grade_level: 建议年级
- knowledge_point: 考纲知识点（原名，存储层用）
- q_type: single / judge / program
- content / answer / difficulty(1-5) / explanation
- program 题: program_lang="python", grading_rules 为 JSON 字符串
  grading_rules 格式: {"language":"python","time_limit":2,"memory_limit":128,
                       "test_cases":[{"input":"","expected":"...\\n","hint":"..."}]}

文案规范（对齐 AGENTS.md）：
- Python 题目面对 3 年级~初三学生，必须保持技术术语准确（print/input/for/if 等不可替换）
- 解析用相对易懂的方式解释原理，低级别（L1-L2）语气更友好
"""
import json


def _py_grading(test_cases, time_limit=2, memory_limit=128):
    """生成 Python 编程题 grading_rules JSON 字符串。

    Args:
        test_cases: [{"input":"...", "expected":"...", "hint":"..."}, ...]
        time_limit: 秒
        memory_limit: MB
    """
    return json.dumps(
        {
            "language": "python",
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "test_cases": test_cases,
        },
        ensure_ascii=False,
    )


# =========================================================================
# Python L1（27 题）：普及（简单数学运算与Turtle库）
# 知识点：编程环境与基础语法 / 输入输出 / 变量与数据类型 / 数学运算 / Turtle绘图 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L1_QUESTIONS = [
    # =============== L1 · 编程环境与基础语法（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "编程环境与基础语法",
        "q_type": "single",
        "content": "在 Python 里，想让屏幕显示一句话，用哪个命令？A.print() B.show() C.display() D.echo()",
        "answer": "A", "difficulty": 1,
        "explanation": "print() 是 Python 的「打印」命令，能把文字、数字显示在屏幕上～show/display/echo 都不是 Python 的输出命令哦。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "编程环境与基础语法",
        "q_type": "single",
        "content": "Python 里表示「文字」要用什么包起来？A.引号（单引号或双引号） B.小括号 C.方括号 D.尖括号",
        "answer": "A", "difficulty": 1,
        "explanation": "文字（字符串）要用引号包起来，单引号'你好'或双引号\"你好\"都行～小括号是运算优先级，方括号是列表，尖括号不是 Python 语法。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "编程环境与基础语法",
        "q_type": "single",
        "content": "Python 一行写完一条语句，需要加分号吗？A.不用加分号 B.必须加分号 C.加逗号 D.加句号",
        "answer": "A", "difficulty": 1,
        "explanation": "Python 不用分号！换行就表示一句话说完了～这跟 C++/Java 不一样，写起来更轻松。分号可以加但没必要。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "编程环境与基础语法",
        "q_type": "judge",
        "content": "Python 代码靠「缩进」（行首的空格）来表示代码块，不是用花括号 {}。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！Python 用缩进（行首空格）表示「这段代码属于谁」～比如 if 里的语句要缩进 4 个空格。这是 Python 最特别的地方！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "编程环境与基础语法",
        "q_type": "judge",
        "content": "Python 的注释（给程序员看的说明）用 # 开头。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！# 后面的内容电脑会忽略，是给人看的说明～写注释能让代码更易懂，是好习惯！",
    },

    # =============== L1 · 输入输出（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "输入输出",
        "q_type": "single",
        "content": "想从键盘读入用户输入的名字，用哪个命令？A.input() B.read() C.get() D.scan()",
        "answer": "A", "difficulty": 1,
        "explanation": "input() 是 Python 的「输入」命令，会等用户打字然后读进来～read/get/scan 都不是 Python 的输入命令。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "输入输出",
        "q_type": "single",
        "content": "input() 读进来的数据是什么类型？A.字符串（str） B.整数（int） C.小数（float） D.随便看输入",
        "answer": "A", "difficulty": 2,
        "explanation": "input() 不管你输入什么，都当成文字（字符串）～输入 10 也是字符串'10'，想做数学运算得先 int() 转成数字！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "输入输出",
        "q_type": "single",
        "content": "print('Hello', 'World') 输出什么？A.Hello World（中间有个空格） B.HelloWorld C.Hello,World D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "print() 用逗号隔开多个内容，输出时默认用空格连接～所以输出「Hello World」（中间有空格）。想连起来用 + 或 sep=''。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "输入输出",
        "q_type": "judge",
        "content": "input('请输入名字：') 里的文字会显示在屏幕上提示用户。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！input() 括号里的文字是「提示语」，会先显示再等输入～这样用户就知道该输什么啦，超贴心！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "输入输出",
        "q_type": "judge",
        "content": "print 默认输出后会换行。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！print 输出完会自动换行～想不换行用 print(..., end='')，end 参数控制结尾。",
    },

    # =============== L1 · 变量与数据类型（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "在 Python 里给变量赋值用哪个符号？A.= B.== C.:= D.<-",
        "answer": "A", "difficulty": 1,
        "explanation": "= 是「赋值」，把右边的值给左边的变量～a = 5 就是把 5 给 a。== 是「判断相等」，:= 是海象运算符（高级），<- 不是 Python 语法。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "name = '小明' 这句里，name 是什么？A.变量 B.字符串 C.函数 D.命令",
        "answer": "A", "difficulty": 1,
        "explanation": "name 是变量名，'小明' 是存进去的值～变量就像贴了标签的盒子，name 这个盒子里装着'小明'。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "想把字符串 '5' 变成整数 5 做数学运算，用哪个？A.int('5') B.str('5') C.float('5') D.print('5')",
        "answer": "A", "difficulty": 2,
        "explanation": "int() 把字符串转成整数～int('5') = 5，就能做数学运算了。str() 是反过来转成字符串，float() 转小数，print() 是输出不是转换。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "变量与数据类型",
        "q_type": "judge",
        "content": "Python 里变量要先声明类型才能用（如 int a = 5）。",
        "answer": "false", "difficulty": 2,
        "explanation": "错！Python 不用先声明类型，直接 a = 5 就行～Python 会自动判断类型，这叫「动态类型」，比 C++/Java 省事！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "judge",
        "content": "a = 5 后再写 a = 'hello' 是允许的，变量类型可以变。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！Python 变量可以随时换类型～先存数字 5，再存文字'hello'，完全没问题。这是动态语言的特点。",
    },

    # =============== L1 · 数学运算（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 3, "knowledge_point": "数学运算",
        "q_type": "single",
        "content": "Python 里算 7 除以 2 等于几？A.3.5 B.3 C.2 D.4",
        "answer": "A", "difficulty": 1,
        "explanation": "Python 里 / 是「真除法」，7 / 2 = 3.5（带小数）～这跟 C++ 的整数除法不一样！想要整数除法用 //（7 // 2 = 3）。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "数学运算",
        "q_type": "single",
        "content": "10 // 3 的结果是？A.3 B.3.33 C.4 D.1",
        "answer": "A", "difficulty": 2,
        "explanation": "// 是「整除」（向下取整）～10 // 3 = 3（丢掉小数部分）。想要余数用 %（10 % 3 = 1），想要小数用 /（10/3 = 3.33...）。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "数学运算",
        "q_type": "judge",
        "content": "** 是 Python 的乘方运算符，2 ** 3 = 8。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！** 是乘方～2 ** 3 = 2×2×2 = 8。这跟 C++ 不同（C++ 用 pow 函数），Python 直接用 ** 更方便！",
    },

    # =============== L1 · Turtle绘图（2 单选 + 1 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "Turtle绘图",
        "q_type": "single",
        "content": "用 Turtle 画图，让小海龟前进 100 步用哪个命令？A.forward(100) B.move(100) C.go(100) D.walk(100)",
        "answer": "A", "difficulty": 2,
        "explanation": "forward(100) 让海龟前进 100 步～move/go/walk 都不是 Turtle 的命令。Turtle 就像指挥一只拿笔的小海龟画画！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "Turtle绘图",
        "q_type": "single",
        "content": "让 Turtle 海龟右转 90 度，用哪个命令？A.right(90) B.turn(90) C.rotate(90) D.right_turn(90)",
        "answer": "A", "difficulty": 2,
        "explanation": "right(90) 让海龟右转 90 度～left(90) 是左转。turn/rotate/right_turn 都不是 Turtle 命令。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "Turtle绘图",
        "q_type": "judge",
        "content": "用 Turtle 画图前，需要先 import turtle 把工具箱搬进来。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！turtle 是 Python 自带的画图工具箱，用之前要 import turtle～然后 t = turtle.Turtle() 创建一只海龟开始画画！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "Turtle绘图",
        "q_type": "program", "program_lang": "python",
        "content": "用 Turtle 画一个正方形：边长 100，画完关闭窗口。\\n要求：import turtle，创建 Turtle 对象，重复 4 次（forward(100) + right(90)）。",
        "answer": "see_grading_rules", "difficulty": 2,
        "explanation": "import turtle → t = turtle.Turtle() → 重复 4 次：t.forward(100) + t.right(90) → turtle.done()～正方形 = 4 条边 + 每次转 90 度，Turtle 画图入门题！",
        "grading_rules": _py_grading([
            {"input": "", "expected": "", "hint": "此题检查代码结构，不产生标准输出"},
        ]),
    },

    # =============== L1 · 综合应用（2 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面代码输出什么？\\n  a = 3\\n  b = 5\\n  print(a + b)\\nA.8 B.35 C.a+b D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "a 存 3，b 存 5，a + b = 8，print 输出 8～不是 35（字符串拼接才会），也不是 a+b（那是没加引号的变量名）。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "name = input('你叫什么？')  print('你好，' + name)  如果输入「小明」，输出什么？A.你好，小明 B.你好，name C.小明 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "input 读进'小明'给 name，'你好，' + name 把两段文字拼起来 = '你好，小明'～+ 在字符串之间是「拼接」！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "print('3' + '5') 的输出是 '35'（文字拼接）。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！'3' 和 '5' 是字符串（有引号），+ 在字符串之间是「拼接」～所以 '3' + '5' = '35'。想算 3+5=8 要用 int() 转成数字！",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "Python 程序从上到下按顺序执行每一行。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！顺序结构是最基础的～程序从上往下一行行跑，先写的先执行。后面才会学分支（if）和循环（for）改变顺序。",
    },
    {
        "syllabus_version": "python-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "python",
        "content": "从键盘读入两个整数 a 和 b（分两行输入），输出它们的和。\\n输入格式：第一行 a，第二行 b。\\n输出格式：一个整数 a+b。",
        "answer": "see_grading_rules", "difficulty": 2,
        "explanation": "a = int(input()) 读第一行转整数，b = int(input()) 读第二行转整数，print(a + b) 输出和～记得 input() 读进来是字符串要 int() 转换！",
        "grading_rules": _py_grading([
            {"input": "3\n5\n", "expected": "8\n", "hint": "3+5=8"},
            {"input": "10\n20\n", "expected": "30\n", "hint": "10+20=30"},
            {"input": "-1\n1\n", "expected": "0\n", "hint": "负数加正数"},
        ]),
    },
]


# =========================================================================
# Python L2（27 题）：基础（核心数据类型：列表、元组、字符串、字典）
# 知识点：分支结构 / 循环结构 / 列表 / 元组与字符串 / 字典 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L2_QUESTIONS = [
    # =============== L2 · 分支结构（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "分支结构",
        "q_type": "single",
        "content": "Python 里 if 语句的格式是？A.if 条件: （冒号结尾，下一行缩进） B.if (条件) { } C.if 条件 then D.if 条件 begin",
        "answer": "A", "difficulty": 2,
        "explanation": "Python 的 if 用「冒号 + 缩进」～if 条件: 然后下一行缩进 4 空格写要做的事。没有括号和花括号，这是 Python 的特色！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "分支结构",
        "q_type": "single",
        "content": "做「分数≥60 显示及格，否则显示不及格」，用哪个？A.if-else B.if C.for D.while",
        "answer": "A", "difficulty": 2,
        "explanation": "有两种情况要用 if-else～if 分数 >= 60: print('及格') else: print('不及格')。if 只管一种，for/while 是循环不是分支！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "分支结构",
        "q_type": "single",
        "content": "多种情况判断（如 90-100 优秀，60-89 及格，<60 不及格）用哪个？A.if-elif-else B.多个 if C.while D.for",
        "answer": "A", "difficulty": 3,
        "explanation": "多种互斥情况用 if-elif-else～elif 是「else if」的缩写。比写多个 if 清晰，且互斥（只走一条路），是分支进阶用法！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "分支结构",
        "q_type": "judge",
        "content": "if 语句后面必须加冒号 :。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！if/elif/else 后面都要加冒号～这是 Python 的语法规定，漏了会报语法错误。冒号表示「下面有代码块」。",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "分支结构",
        "q_type": "judge",
        "content": "if 条件:  下面的语句可以不缩进，跟 if 对齐就行。",
        "answer": "false", "difficulty": 2,
        "explanation": "错！if 下的语句必须缩进（行首加 4 空格）～不缩进 Python 就认为不属于 if，会报错或逻辑错误。缩进是 Python 的灵魂！",
    },

    # =============== L2 · 循环结构（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "循环结构",
        "q_type": "single",
        "content": "想重复 5 次，用哪个循环最方便？A.for i in range(5) B.while 5 C.repeat 5 D.loop 5",
        "answer": "A", "difficulty": 2,
        "explanation": "for i in range(5) 是 Python 的固定次数循环～range(5) 生成 0,1,2,3,4，循环 5 次。repeat/loop 不是 Python 语法，while 要自己控制。",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "循环结构",
        "q_type": "single",
        "content": "range(1, 6) 生成哪些数字？A.1, 2, 3, 4, 5 B.1, 2, 3, 4, 5, 6 C.0, 1, 2, 3, 4, 5 D.1 到 6",
        "answer": "A", "difficulty": 2,
        "explanation": "range(1, 6) 从 1 开始到 6 之前（不含 6）～生成 1,2,3,4,5。range 是「左闭右开」，记住不含结尾！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "循环结构",
        "q_type": "single",
        "content": "不知道循环几次，只知道「直到某条件成立才停」，用哪个？A.while B.for C.if D.break",
        "answer": "A", "difficulty": 3,
        "explanation": "while 适合「条件成立就一直做」的不定次循环～for 是固定次数。while 条件: 满足就继续，不满足就退出。",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "循环结构",
        "q_type": "judge",
        "content": "for i in range(3): 循环 3 次，i 的值是 0、1、2。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！range(3) 生成 0,1,2（从 0 开始，不含 3）～i 依次取 0、1、2，循环 3 次。Python 计数从 0 开始！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "循环结构",
        "q_type": "judge",
        "content": "break 用来跳出循环，continue 用来跳过本次剩余语句进入下一次循环。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！break 是「破门而出」直接结束整个循环；continue 是「跳过这次」进入下一轮～两个都是循环控制语句，很常用！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "循环结构",
        "q_type": "program", "program_lang": "python",
        "content": "计算 1 到 10 的和并输出。\\n要求：用 for 循环 + range，求 1+2+...+10。",
        "answer": "see_grading_rules", "difficulty": 2,
        "explanation": "s = 0 → for i in range(1, 11): s += i → print(s)～range(1,11) 是 1 到 10，累加到 s，最后输出 55。循环求和经典题！",
        "grading_rules": _py_grading([
            {"input": "", "expected": "55\n", "hint": "1+2+...+10=55"},
        ]),
    },

    # =============== L2 · 列表（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l2", "grade_level": 4, "knowledge_point": "列表",
        "q_type": "single",
        "content": "创建一个列表 [1, 2, 3]，用哪个？A.[1, 2, 3] B.(1, 2, 3) C.{1, 2, 3} D.<1, 2, 3>",
        "answer": "A", "difficulty": 2,
        "explanation": "列表用方括号 []～[1, 2, 3] 是列表。小括号()是元组，花括号{}是字典或集合，尖括号不是 Python 语法。",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "列表",
        "q_type": "single",
        "content": "列表 a = [10, 20, 30]，a[0] 是什么？A.10 B.20 C.30 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "Python 列表从 0 开始编号～a[0] 是第 1 个 = 10，a[1] 是 20，a[2] 是 30。记住：第 n 个的下标是 n-1！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "列表",
        "q_type": "single",
        "content": "往列表末尾添加新数据 5，用哪个？A.a.append(5) B.a.add(5) C.a.push(5) D.a.insert(5)",
        "answer": "A", "difficulty": 2,
        "explanation": "append() 在列表末尾加一个数据～add/push 不是列表方法，insert 要指定位置。append 是列表最常用的增删方法！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "列表",
        "q_type": "judge",
        "content": "列表里的数据可以是不同类型（如 [1, 'hello', 3.14]）。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！Python 列表能混装不同类型～[1, 'hello', 3.14] 完全合法。这跟有些语言（数组要同类型）不一样，Python 超灵活！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "列表",
        "q_type": "judge",
        "content": "len([1, 2, 3]) 返回 3，表示列表有 3 个数据。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！len() 数列表有几个数据～[1,2,3] 有 3 个，len 返回 3。也适用于字符串、元组等，是超常用的函数！",
    },

    # =============== L2 · 元组与字符串（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "元组与字符串",
        "q_type": "single",
        "content": "元组和列表最大的区别是？A.元组创建后不能改，列表能改 B.元组用[]，列表用() C.元组更快 D.没区别",
        "answer": "A", "difficulty": 3,
        "explanation": "元组（tuple）是「不可变」的，创建后不能增删改～列表（list）能改。元组用()，列表用[]。不可变更安全，适合存不变的数据！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "元组与字符串",
        "q_type": "single",
        "content": "s = 'hello'，s[1] 是什么？A.'e' B.'h' C.'l' D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "字符串也能用下标取字符～s[0]='h', s[1]='e', s[2]='l'...字符串跟列表一样从 0 开始编号！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "元组与字符串",
        "q_type": "single",
        "content": "s = 'Python'，s[0:3] 返回什么？A.'Pyt' B.'Pyth' C.'yth' D.'Python'",
        "answer": "A", "difficulty": 3,
        "explanation": "s[0:3] 是「切片」，取下标 0 到 3 之前（不含 3）～即 'Pyt'。切片是「左闭右开」，记住不含结尾下标！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "元组与字符串",
        "q_type": "judge",
        "content": "字符串创建后不能修改某个字符（如 s[0] = 'a' 会报错）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！字符串是不可变的～想改要用切片拼接：s = 'a' + s[1:]。这跟列表（可改）不一样，字符串像元组一样固定。",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "元组与字符串",
        "q_type": "judge",
        "content": "'hello'.upper() 返回 'HELLO'（全大写）。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！upper() 把字符串全转大写～lower() 转全小写。这是字符串的常用方法，做大小写转换超方便！",
    },

    # =============== L2 · 字典（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "single",
        "content": "字典用哪个符号？A.花括号 {} B.方括号 [] C.小括号 () D.尖括号 <>",
        "answer": "A", "difficulty": 2,
        "explanation": "字典用花括号 {}～{':苹果', 'name':'小明'} 是字典。方括号是列表，小括号是元组。字典存「键值对」，像查字典！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "single",
        "content": "d = {'name': '小明', 'age': 10}，怎么取出名字？A.d['name'] B.d.name C.d[0] D.d{'name'}",
        "answer": "A", "difficulty": 2,
        "explanation": "字典用「键」查「值」～d['name'] = '小明'。不是 d.name（那是属性访问）或 d[0]（字典没编号，用键不用下标）！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "single",
        "content": "字典和列表的最大区别是？A.字典用「键」查值，列表用「下标」查值 B.字典只能存数字 C.列表更快 D.没区别",
        "answer": "A", "difficulty": 3,
        "explanation": "字典是「键值对」，用有意义的键（如'name'）查值～列表用数字下标（如 0,1）查值。字典适合存「有名字的数据」，像资料卡！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "judge",
        "content": "字典里的键必须唯一，不能重复。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！字典的键不能重复～如果重复，后面的会覆盖前面的。就像查字典同一个词只有一个解释，不能有好几个！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "judge",
        "content": "字典 d = {'a': 1}，可以用 d['b'] = 2 添加新的键值对。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！给字典不存在的键赋值就是「添加」～d['b'] = 2 会新增 'b': 2。这跟列表（要用 append）不一样，字典直接赋值就行！",
    },
    {
        "syllabus_version": "python-l2", "grade_level": 5, "knowledge_point": "字典",
        "q_type": "program", "program_lang": "python",
        "content": "从键盘读入 3 个同学的名字和分数（分 3 行，每行「名字 分数」），存入字典，然后输出分数最高的同学名字。\\n输入：3 行，每行「名字 分数」（分数是整数）。\\n输出：分数最高的同学名字。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "用循环读 3 行，split() 拆名字和分数，存入字典 d[名字]=int(分数)～然后用 max(d, key=d.get) 找分数最高的键（名字）。字典+max的经典用法！",
        "grading_rules": _py_grading([
            {"input": "小明 90\n小红 85\n小刚 95\n", "expected": "小刚\n", "hint": "小刚 95 分最高"},
            {"input": "a 10\nb 20\nc 5\n", "expected": "b\n", "hint": "b 20 分最高"},
        ]),
    },
]


# =========================================================================
# Python L3（27 题）：算法入门
# 知识点：组合数据类型 / 解析算法 / 枚举算法 / 排序算法 / 查找算法 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L3_QUESTIONS = [
    # =============== L3 · 组合数据类型（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "组合数据类型",
        "q_type": "single",
        "content": "集合（set）的特点是？A.元素唯一、无序 B.元素可重复 C.有序 D.用[]创建",
        "answer": "A", "difficulty": 3,
        "explanation": "集合用{}创建，元素唯一（重复自动去重）、无序～{1,2,3} 和 {3,2,1} 是同一个集合。适合去重和成员判断！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "组合数据类型",
        "q_type": "single",
        "content": "想列表去重（去掉重复），最快的方法是？A.list(set(a)) B.for 循环判断 C.用 sort() D.用 append()",
        "answer": "A", "difficulty": 3,
        "explanation": "set 自动去重，list(set(a)) 一行搞定～for 循环判断太慢，sort 只排序不去重，append 是添加不是去重。集合去重是经典技巧！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "组合数据类型",
        "q_type": "single",
        "content": "列表推导式 [x*2 for x in range(3)] 的结果是？A.[0, 2, 4] B.[2, 4, 6] C.[0, 1, 2] D.[0, 2, 4, 6]",
        "answer": "A", "difficulty": 3,
        "explanation": "range(3) 是 0,1,2，每个 x*2 得 0,2,4～列表推导式是「一行生成列表」的简洁写法，超实用！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "组合数据类型",
        "q_type": "judge",
        "content": "集合 {1, 2, 3} 和 {3, 2, 1} 是相等的。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！集合无序，只要元素一样就相等～{1,2,3} == {3,2,1} 为 True。这跟列表不同（列表有序）。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "组合数据类型",
        "q_type": "judge",
        "content": "列表推导式比 for 循环 + append 更简洁，但运行结果一样。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！[x*2 for x in range(3)] 等价于 a=[]; for x in range(3): a.append(x*2)～推导式更简洁，Pythonic 风格！",
    },

    # =============== L3 · 解析算法（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "解析算法",
        "q_type": "single",
        "content": "「解析算法」是指？A.用数学公式直接计算结果 B.一个个试 C.排序 D.查找",
        "answer": "A", "difficulty": 3,
        "explanation": "解析算法是「套公式直接算」～如求圆面积 S=πr²，直接用公式算。比枚举（一个个试）快，但要有现成公式！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "解析算法",
        "q_type": "single",
        "content": "求一元二次方程 ax²+bx+c=0 的根，用解析算法的核心是？A.套求根公式 x=(-b±√(b²-4ac))/(2a) B.枚举所有 x C.排序 D.二分查找",
        "answer": "A", "difficulty": 3,
        "explanation": "有现成公式就套公式～求根公式直接算出根，比枚举（试无数个 x）快无数倍！这就是解析算法的威力。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "解析算法",
        "q_type": "judge",
        "content": "解析算法适合「有明确数学公式」的问题。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！有公式就能用解析算法直接算～没公式就只能用枚举（穷举）一个个试。解析快但要公式，枚举慢但通用。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "解析算法",
        "q_type": "judge",
        "content": "解析算法的效率通常比枚举算法高。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！解析是 O(1) 套公式秒出结果，枚举是 O(n) 或更高一个个试～有公式就用解析，快得多！",
    },

    # =============== L3 · 枚举算法（2 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "枚举算法",
        "q_type": "single",
        "content": "枚举算法（穷举）的核心思想是？A.把所有可能一个个试，找到满足条件的 B.套公式 C.排序后找 D.二分",
        "answer": "A", "difficulty": 3,
        "explanation": "枚举就是「一个不漏地试」～把所有可能列举出来，判断哪些满足条件。慢但通用，没公式时用它！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "枚举算法",
        "q_type": "single",
        "content": "找 100 以内所有 3 的倍数，用枚举怎么写？A.for i in range(101): if i%3==0 B.while True C.print(3*1, 3*2...) D.用公式",
        "answer": "A", "difficulty": 3,
        "explanation": "枚举 0 到 100 每个数，判断 i%3==0 就是 3 的倍数～这是经典枚举！用 for+if 一行行试，找出所有满足的。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "枚举算法",
        "q_type": "judge",
        "content": "枚举算法一定能找到所有解，但可能很慢。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！枚举「不漏」所以能找全，但「不重」地试所有可能很费时～数据量大时慢，小数据没问题。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "枚举算法",
        "q_type": "judge",
        "content": "枚举算法适合「搜索空间小」的问题，空间太大不现实。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！枚举是 O(n) 或更高，数据量一大就爆炸～如找 1000 以内的数可以，找 10 亿以内的就太慢。大问题要用更聪明的算法！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "枚举算法",
        "q_type": "program", "program_lang": "python",
        "content": "找出 100 以内所有「既是 3 的倍数又是 5 的倍数」的数，每行输出一个。\\n要求：用枚举，判断 i%3==0 and i%5==0。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "for i in range(1, 101): if i%3==0 and i%5==0: print(i)～3 和 5 的公倍数即 15 的倍数：15,30,45,60,75,90。枚举+条件判断经典题！",
        "grading_rules": _py_grading([
            {"input": "", "expected": "15\n30\n45\n60\n75\n90\n", "hint": "15的倍数：15,30,45,60,75,90"},
        ]),
    },

    # =============== L3 · 排序算法（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 6, "knowledge_point": "排序算法",
        "q_type": "single",
        "content": "Python 内置的排序函数是？A.sorted() 和 list.sort() B.order() C.arrange() D.sort_list()",
        "answer": "A", "difficulty": 2,
        "explanation": "sorted(a) 返回新排序列表（不改原列表），a.sort() 原地排序（改原列表）～order/arrange/sort_list 都不是 Python 函数。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "排序算法",
        "q_type": "single",
        "content": "冒泡排序每次比较相邻两个，把大的往后冒，一趟下来最大的在最后～它的平均时间复杂度是？A.O(n²) B.O(n) C.O(n log n) D.O(1)",
        "answer": "A", "difficulty": 3,
        "explanation": "冒泡两层循环，平均和最坏都是 O(n²)～慢但简单。O(n log n) 是快排/归并，O(n) 是线性，O(1) 是常数。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "排序算法",
        "q_type": "single",
        "content": "想降序排序，sorted(a, ?) 的问号处填什么？A.reverse=True B.desc=True C.order='desc' D.-1",
        "answer": "A", "difficulty": 3,
        "explanation": "sorted(a, reverse=True) 降序～reverse 参数默认 False（升序），设 True 就反过来（降序）。这是最方便的降序方法！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "排序算法",
        "q_type": "judge",
        "content": "sorted(a) 返回新列表，不改原列表；a.sort() 改原列表，返回 None。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！sorted() 是「新建」一个排好的列表，原列表不动；.sort() 是「原地」改，原列表变有序。想保留原数据用 sorted！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "排序算法",
        "q_type": "judge",
        "content": "冒泡排序是稳定排序（相等的元素相对顺序不变）。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！冒泡只交换「严格大于」的相邻对，相等的不动～所以相等元素的相对顺序保持不变，是稳定排序。快排不稳定！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "排序算法",
        "q_type": "program", "program_lang": "python",
        "content": "读入一行用空格隔开的整数，排序后从小到大输出（用空格隔开）。\\n输入：一行若干整数，空格隔开。\\n输出：从小到大排序，空格隔开。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "a = list(map(int, input().split())) 读入转整数列表 → a.sort() 排序 → print(' '.join(map(str, a))) 输出～split+map+sort+join 是经典套路！",
        "grading_rules": _py_grading([
            {"input": "3 1 4 1 5 9 2 6\n", "expected": "1 1 2 3 4 5 6 9\n", "hint": "排序结果"},
            {"input": "5 4 3 2 1\n", "expected": "1 2 3 4 5\n", "hint": "逆序变正序"},
        ]),
    },

    # =============== L3 · 查找算法（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "查找算法",
        "q_type": "single",
        "content": "在列表里找某个值，最简单的「顺序查找」时间复杂度是？A.O(n) B.O(1) C.O(log n) D.O(n²)",
        "answer": "A", "difficulty": 3,
        "explanation": "顺序查找从头到尾一个个比，最坏要找 n 次～O(n)。O(log n) 是二分查找（要有序），O(1) 是直接定位。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "查找算法",
        "q_type": "single",
        "content": "二分查找的前提是？A.列表必须有序 B.列表必须无序 C.列表必须很大 D.列表必须很小",
        "answer": "A", "difficulty": 3,
        "explanation": "二分查找要「有序」才能每次砍一半～无序没法判断往左还是往右找。有序+二分 = O(log n)，超快！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "查找算法",
        "q_type": "judge",
        "content": "二分查找每次把搜索范围砍一半，效率是 O(log n)。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！二分每次取中间比较，砍掉一半～n 个数据最多找 log₂n 次。100 万数据只需 20 次，超快！但必须有序。",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "查找算法",
        "q_type": "judge",
        "content": "in 运算符（如 5 in [1,2,3]）本质是顺序查找。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！列表的 in 是 O(n) 顺序查找～一个个比。但集合/字典的 in 是 O(1) 哈希查找，超快。所以频繁查找用集合！",
    },

    # =============== L3 · 综合应用（3 单选 + 0 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "统计列表 [1,2,2,3,3,3] 中每个数字出现次数，最方便用什么？A.字典（键是数字，值是次数） B.列表 C.元组 D.集合",
        "answer": "A", "difficulty": 3,
        "explanation": "字典 d[num] = d.get(num, 0) + 1 统计次数～{1:1, 2:2, 3:3}。字典适合「计数」场景，键是元素，值是次数！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面代码输出什么？\\n  a = [3, 1, 2]\\n  a.sort()\\n  print(a)\\nA.[1, 2, 3] B.[3, 2, 1] C.[3, 1, 2] D.None",
        "answer": "A", "difficulty": 2,
        "explanation": "a.sort() 原地升序排序，a 变成 [1,2,3]～print 输出 [1, 2, 3]。sort 改原列表，不返回新列表！",
    },
    {
        "syllabus_version": "python-l3", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "想把列表 a = [1,2,3,4,5] 反转（变成 [5,4,3,2,1]），用哪个？A.a.reverse() 或 a[::-1] B.a.sort() C.a.flip() D.a.revert()",
        "answer": "A", "difficulty": 3,
        "explanation": "a.reverse() 原地反转，a[::-1] 切片反转返回新列表～sort 是排序不是反转，flip/revert 不是列表方法。反转用 reverse 或切片！",
    },
]


# =========================================================================
# Python L4（27 题）：进阶（函数、文件、异常处理）
# 知识点：函数定义与调用 / 参数与返回值 / 文件操作 / 异常处理 / 模块与包 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L4_QUESTIONS = [
    # =============== L4 · 函数定义与调用（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "Python 用哪个关键字定义函数？A.def B.function C.func D.define",
        "answer": "A", "difficulty": 2,
        "explanation": "def 是「define」的缩写～def 函数名(): 定义函数。function/func/define 都不是 Python 关键字。def 是 Python 的函数定义关键字！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "函数的「返回值」用哪个关键字？A.return B.send C.give D.output",
        "answer": "A", "difficulty": 2,
        "explanation": "return 把结果送出函数～return 5 表示函数返回 5。没 return 的函数返回 None。send/give/output 都不是 Python 关键字！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "下面函数调用输出什么？\\n  def add(a, b):\\n      return a + b\\n  print(add(3, 5))\\nA.8 B.35 C.None D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "add(3,5) 把 3 给 a，5 给 b，return a+b=8～print 输出 8。函数把 a+b 的结果返回给调用处！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "judge",
        "content": "函数定义后必须调用才会执行里面的代码。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！def 只是「定义」函数，告诉电脑有这个函数～要函数名() 调用才会真正执行。定义了不调用，里面的代码不跑！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "函数定义与调用",
        "q_type": "judge",
        "content": "函数没有 return 语句时，返回 None。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！没 return 或 return 后面没值，函数都返回 None～None 是 Python 的「空值」，表示「什么都没有」。调用这种函数拿不到有用结果！",
    },

    # =============== L4 · 参数与返回值（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "single",
        "content": "def f(a, b=10): 里 b 是什么参数？A.默认参数（不传就用 10） B.必填参数 C.可变参数 D.关键字参数",
        "answer": "A", "difficulty": 3,
        "explanation": "b=10 是「默认参数」～调用 f(5) 时 b 用默认值 10，调用 f(5, 20) 时 b=20。默认参数让调用更灵活！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "single",
        "content": "*args 和 **kwargs 的区别是？A.*args 收集位置参数（元组），**kwargs 收集关键字参数（字典） B.没区别 C.*args 收集字典 D.**kwargs 收集列表",
        "answer": "A", "difficulty": 4,
        "explanation": "*args 把多余的位置参数打包成元组，**kwargs 把多余的关键字参数打包成字典～让函数能接受任意数量参数，超灵活！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "single",
        "content": "函数可以返回多个值吗？A.可以，如 return a, b（实际返回元组） B.不行，只能一个 C.只能返回列表 D.会报错",
        "answer": "A", "difficulty": 3,
        "explanation": "可以！return a, b 实际返回元组 (a, b)～用 x, y = func() 解包接收。Python 这个特性超方便，多个值一起返回！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "judge",
        "content": "默认参数必须放在普通参数后面（如 def f(a, b=10) 不能 def f(b=10, a)）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！默认参数要在后面～因为调用时按位置匹配，前面的必填，后面的可省。放前面 Python 不知道你省了哪个，会报错！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "judge",
        "content": "return a, b 返回的是一个元组，可以用 x, y = func() 解包。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！return a, b 实际是 return (a, b) 元组～用 x, y = func() 自动解包，x 拿 a，y 拿 b。多返回值+解包是 Python 特色！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "参数与返回值",
        "q_type": "program", "program_lang": "python",
        "content": "定义函数 is_prime(n) 判断 n 是否为素数（只能被 1 和自己整除的大于 1 的整数），是返回 True，否返回 False。读入一个整数，输出 Yes 或 No。\\n输入：一个整数 n。\\n输出：Yes（素数）或 No（非素数）。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "def is_prime(n): if n<2: return False; for i in range(2, int(n**0.5)+1): if n%i==0: return False; return True～用函数封装判断逻辑，main 调用输出。函数+枚举经典！",
        "grading_rules": _py_grading([
            {"input": "7\n", "expected": "Yes\n", "hint": "7 是素数"},
            {"input": "4\n", "expected": "No\n", "hint": "4=2×2 非素数"},
            {"input": "1\n", "expected": "No\n", "hint": "1 不是素数"},
        ]),
    },

    # =============== L4 · 文件操作（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "single",
        "content": "打开文件用哪个函数？A.open() B.read() C.file() D.fopen()",
        "answer": "A", "difficulty": 2,
        "explanation": "open('文件名', '模式') 打开文件～read/file/fopen 都不是。open 返回文件对象，然后用 .read()/.write() 读写。",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "single",
        "content": "open('a.txt', 'w') 的 'w' 模式是？A.写（覆盖原有内容） B.读 C.追加 D.二进制",
        "answer": "A", "difficulty": 2,
        "explanation": "'w' 是 write 写模式，会清空原内容重写～'r' 读，'a' 追加（不清空，加末尾），'b' 二进制。写文件要小心别覆盖重要数据！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "single",
        "content": "with open('a.txt') as f: 的好处是？A.用完自动关闭文件，不用手动 f.close() B.读得更快 C.能加密 D.能压缩",
        "answer": "A", "difficulty": 3,
        "explanation": "with 语句会在代码块结束时自动关闭文件～即使出错也能关，超安全。不用 with 要手动 f.close()，容易忘！这是 Python 推荐写法。",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "judge",
        "content": "open('a.txt', 'r') 如果文件不存在会报错。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！读模式 'r' 文件不存在会抛 FileNotFoundError～写模式 'w' 不存在会自动创建。读要小心文件路径！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "judge",
        "content": "f.read() 一次读完整个文件，f.readline() 读一行。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！read() 全读成一个字符串，readline() 每次读一行～大文件用 readline 或 for line in f 逐行读，省内存！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "文件操作",
        "q_type": "program", "program_lang": "python",
        "content": "读入一行文本，统计其中单词数（用空格分隔），输出单词个数。\\n输入：一行文本。\\n输出：单词个数（整数）。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "s = input() → words = s.split() → print(len(words))～split() 默认按空格拆分，len() 数个数。字符串处理经典题！",
        "grading_rules": _py_grading([
            {"input": "hello world python\n", "expected": "3\n", "hint": "3 个单词"},
            {"input": "one\n", "expected": "1\n", "hint": "1 个单词"},
        ]),
    },

    # =============== L4 · 异常处理（3 单选 + 2 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "异常处理",
        "q_type": "single",
        "content": "Python 异常处理用哪组关键字？A.try-except B.if-else C.for-in D.begin-end",
        "answer": "A", "difficulty": 2,
        "explanation": "try 包住可能出错的代码，except 捕获错误～比让程序崩溃友好。try-except 是 Python 异常处理的核心结构！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "异常处理",
        "q_type": "single",
        "content": "10 / 0 会抛什么异常？A.ZeroDivisionError B.ValueError C.TypeError D.IndexError",
        "answer": "A", "difficulty": 3,
        "explanation": "除以 0 抛 ZeroDivisionError～ValueError 是值不对（如 int('abc')），TypeError 是类型不对，IndexError 是下标越界。",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "异常处理",
        "q_type": "single",
        "content": "try-except-else-finally 里，finally 的代码什么时候执行？A.无论是否出错都执行 B.只在出错时 C.只在不出错时 D.从不执行",
        "answer": "A", "difficulty": 3,
        "explanation": "finally 无论出错与否都执行～常用于关闭文件、释放资源。else 是不出错才执行，except 是出错才执行，finally 必执行！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "异常处理",
        "q_type": "judge",
        "content": "try 里没出错时，except 里的代码不执行。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！try 没出错就跳过 except，走 else（有的话）或 finally～except 只在 try 出错时才执行，是「错误处理」分支。",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "异常处理",
        "q_type": "judge",
        "content": "可以用 except 捕获多种异常，如 except (ValueError, TypeError):。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！用元组把多个异常类型括起来，任意一个发生都进入这个 except～比写多个 except 简洁。是异常处理的常用技巧！",
    },

    # =============== L4 · 模块与包（3 单选 + 2 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "模块与包",
        "q_type": "single",
        "content": "导入模块用哪个关键字？A.import B.include C.require D.use",
        "answer": "A", "difficulty": 2,
        "explanation": "import 模块名 导入～如 import math。include 是 C++，require 是 JS，use 不是 Python 关键字。import 是 Python 导入模块的关键字！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "模块与包",
        "q_type": "single",
        "content": "只导入模块的某个函数，用哪个？A.from 模块 import 函数 B.import 函数 from 模块 C.use 函数 D.include 函数",
        "answer": "A", "difficulty": 3,
        "explanation": "from math import sqrt 只导入 sqrt～之后直接用 sqrt() 不用 math.sqrt()。import math 是导入整个模块，要用 math.sqrt()。",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "模块与包",
        "q_type": "single",
        "content": "给模块起别名用哪个关键字？A.as B.alias C.rename D.name",
        "answer": "A", "difficulty": 3,
        "explanation": "import numpy as np 给 numpy 起别名 np～之后用 np.xxx 代替 numpy.xxx。as 是「作为」的意思，别名让代码更简洁！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "模块与包",
        "q_type": "judge",
        "content": "math.sqrt(16) 返回 4.0（浮点数）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！math.sqrt() 返回浮点数～sqrt(16) = 4.0。想要整数用 int(math.sqrt(16))。math 是数学模块，要用前 import math！",
    },
    {
        "syllabus_version": "python-l4", "grade_level": 8, "knowledge_point": "模块与包",
        "q_type": "judge",
        "content": "random.randint(1, 6) 返回 1 到 6（含两头）的随机整数。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！random.randint(a, b) 返回 [a, b] 含两头的随机整数～randint(1,6) 可能返回 1,2,3,4,5,6。做骰子游戏常用！",
    },
]


# =========================================================================
# Python L5（27 题）：高级语法与标准库
# 知识点：列表推导式 / 生成器与迭代器 / 切片高级 / 解包与星号 / math与random / time模块 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L5_QUESTIONS = [
    # =============== L5 · 列表推导式（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 8, "knowledge_point": "列表推导式",
        "q_type": "single",
        "content": "下面列表推导式结果是什么？ [x**2 for x in range(4)]\nA.[0, 1, 4, 9] B.[0, 1, 4, 9, 16] C.[1, 4, 9, 16] D.[0, 1, 2, 3]",
        "answer": "A", "difficulty": 3,
        "explanation": "range(4) 生成 0,1,2,3，每个 x 平方得 0,1,4,9～列表推导式是 Pythonic 的简洁写法，比 for+append 更优雅！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 8, "knowledge_point": "列表推导式",
        "q_type": "single",
        "content": "想用列表推导式筛出偶数，哪个写法对？\nA.[x for x in a if x%2==0] B.[x if x%2==0 for x in a] C.[for x in a if x%2==0] D.[x for x in a where x%2==0]",
        "answer": "A", "difficulty": 3,
        "explanation": "推导式结构是「表达式 for 变量 in 序列 if 条件」～筛选用 if 放后面。B 顺序错，C 缺表达式，D where 不是 Python 语法！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "列表推导式",
        "q_type": "single",
        "content": "[x for x in range(10) if x%3==0] 的结果是？\nA.[0, 3, 6, 9] B.[3, 6, 9] C.[0, 1, 2, 3] D.[3, 6, 9, 12]",
        "answer": "A", "difficulty": 3,
        "explanation": "range(10) 是 0-9，筛 3 的倍数得 0,3,6,9～注意 0 也是 3 的倍数（0%3==0），别漏掉！推导式+if 筛选超实用。",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 8, "knowledge_point": "列表推导式",
        "q_type": "judge",
        "content": "列表推导式可以嵌套，如 [[j for j in range(3)] for i in range(2)] 生成二维列表。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！嵌套推导式生成 [[0,1,2],[0,1,2]]～外层循环 2 次，每次内层生成 [0,1,2]。复杂但强大，处理矩阵常用！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "列表推导式",
        "q_type": "judge",
        "content": "{x: x**2 for x in range(3)} 是字典推导式，结果是 {0:0, 1:1, 2:4}。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！用花括号 + 键值对就是字典推导式～{0:0, 1:1, 2:4}。还有集合推导式 {x for x in ...}，Python 推导式家族齐全！",
    },

    # =============== L5 · 生成器与迭代器（2 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "生成器与迭代器",
        "q_type": "single",
        "content": "生成器（generator）和列表最大的区别是？\nA.生成器用 () 创建，惰性求值省内存 B.生成器用[]创建 C.生成器能改 D.没区别",
        "answer": "A", "difficulty": 4,
        "explanation": "生成器用 () 创建如 (x for x in range(5))，它「惰性求值」不一次算完，省内存～列表用[]一次算完占内存。处理大数据用生成器！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "生成器与迭代器",
        "q_type": "single",
        "content": "函数里有 yield 关键字，这个函数是？\nA.生成器函数（返回生成器） B.普通函数 C.会报错 D.返回 None",
        "answer": "A", "difficulty": 4,
        "explanation": "yield 让函数变成生成器函数～调用它返回一个生成器对象，每次 next() 执行到 yield 暂停并返回值。比 return 一次返回更灵活！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "生成器与迭代器",
        "q_type": "judge",
        "content": "生成器只能遍历一次，遍历完就空了，不能再次遍历。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！生成器是「一次性」的，遍历完就没了～想多次遍历要重新创建或转成列表。这是惰性求值的代价，省内存但不持久！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "生成器与迭代器",
        "q_type": "judge",
        "content": "for x in g 能遍历生成器 g，跟遍历列表语法一样。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！for 循环能遍历任何「可迭代对象」～列表、元组、字符串、生成器都能用 for。生成器遍历时才真正计算，惰性！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "生成器与迭代器",
        "q_type": "program", "program_lang": "python",
        "content": "用生成器函数生成 0 到 n-1 的平方数列，然后遍历输出每个值（每行一个）。\n输入：一个整数 n。\n输出：n 行，第 i 行（从 0 开始）是 i 的平方。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "def squares(n): for i in range(n): yield i*i → g = squares(n) → for x in g: print(x)～yield 让函数变生成器，惰性产出平方。生成器经典题！",
        "grading_rules": _py_grading([
            {"input": "4\n", "expected": "0\n1\n4\n9\n", "hint": "0,1,4,9"},
            {"input": "3\n", "expected": "0\n1\n4\n", "hint": "0,1,4"},
        ]),
    },

    # =============== L5 · 切片高级（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 8, "knowledge_point": "切片高级",
        "q_type": "single",
        "content": "a = [1,2,3,4,5]，a[1:4] 返回什么？\nA.[2, 3, 4] B.[2, 3, 4, 5] C.[1, 2, 3, 4] D.[3, 4]",
        "answer": "A", "difficulty": 3,
        "explanation": "a[1:4] 取下标 1 到 4 之前（不含 4）～即 a[1],a[2],a[3] = 2,3,4。切片左闭右开，记住不含结尾下标！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "切片高级",
        "q_type": "single",
        "content": "a = [1,2,3,4,5]，a[::-1] 返回什么？\nA.[5, 4, 3, 2, 1]（反转） B.[1, 2, 3, 4, 5] C.报错 D.[5]",
        "answer": "A", "difficulty": 3,
        "explanation": "a[::-1] 步长 -1 表示「倒着走」～反转列表得 [5,4,3,2,1]。切片反转是最 Pythonic 的写法，比 reverse() 更优雅！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "切片高级",
        "q_type": "single",
        "content": "a = [1,2,3,4,5,6]，a[1::2] 返回什么？\nA.[2, 4, 6] B.[1, 3, 5] C.[2, 3, 4, 5, 6] D.[1, 2, 3]",
        "answer": "A", "difficulty": 4,
        "explanation": "a[1::2] 从下标 1 开始，步长 2（跳一个取一个）～取 a[1]=2, a[3]=4, a[5]=6 = [2,4,6]。切片步长超实用！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "切片高级",
        "q_type": "judge",
        "content": "a = [1,2,3]，a[10:] 不会报错，返回空列表 []。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！切片越界不报错，返回空～a[10:] 超出范围返回 []。这跟下标访问 a[10] 不同（a[10] 会 IndexError）。切片很宽容！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "切片高级",
        "q_type": "judge",
        "content": "切片 a[2:5] 创建新列表，修改新列表不影响原列表 a。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！切片是「浅拷贝」，创建新列表～改新列表不影响原列表。想同步改要用 a[2:5] = [...] 赋值，那是「切片赋值」！",
    },

    # =============== L5 · 解包与星号（2 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "解包与星号",
        "q_type": "single",
        "content": "a, b, c = [1, 2, 3] 后，b 是多少？\nA.2 B.1 C.3 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "解包把列表的元素依次给变量～a=1, b=2, c=3。变量数要和元素数一致，否则报错。解包是 Python 的简洁特性！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "解包与星号",
        "q_type": "single",
        "content": "a, *b = [1, 2, 3, 4] 后，b 是什么？\nA.[2, 3, 4]（列表） B.2 C.[1] D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "*b 是「星号解包」，把剩余元素打包成列表～a=1, b=[2,3,4]。* 能收集多余元素，超灵活！处理不定长数据常用。",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "解包与星号",
        "q_type": "judge",
        "content": "*args 在函数参数里收集多余的位置参数成元组。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！def f(*args) 把所有位置参数打包成元组 args～调用 f(1,2,3) 时 args=(1,2,3)。让函数接受任意多参数，超灵活！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "解包与星号",
        "q_type": "judge",
        "content": "a, *b, c = [1, 2, 3, 4, 5] 后，b 是 [2, 3, 4]。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！a=1, c=5, *b 收集中间部分 [2,3,4]～星号变量可以放中间，自动收集「中间多余」的。高级解包技巧！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "解包与星号",
        "q_type": "program", "program_lang": "python",
        "content": "读入一行用空格隔开的整数，第一个数是 n，后面有 n 个数。用解包方式取出后面的 n 个数，输出它们的和。\n输入：一行，第一个是 n，后面 n 个整数，空格隔开。\n输出：后面 n 个数的和。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "nums = list(map(int, input().split())) → n, *rest = nums → 取 rest[:n] 求和 → print(sum(rest[:n]))～解包 + 切片 + sum，综合应用！",
        "grading_rules": _py_grading([
            {"input": "3 10 20 30\n", "expected": "60\n", "hint": "10+20+30=60"},
            {"input": "2 5 15\n", "expected": "20\n", "hint": "5+15=20"},
        ]),
    },

    # =============== L5 · math与random（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 8, "knowledge_point": "math与random",
        "q_type": "single",
        "content": "import math，math.floor(3.7) 返回什么？\nA.3（向下取整） B.4 C.3.7 D.报错",
        "answer": "A", "difficulty": 3,
        "explanation": "math.floor 向下取整～floor(3.7)=3。math.ceil 是向上取整（ceil(3.2)=4）。注意 int(3.7) 也是 3，但负数不同：floor(-3.2)=-4，int(-3.2)=-3！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "math与random",
        "q_type": "single",
        "content": "random.choice([1,2,3]) 的作用是？\nA.随机选一个元素 B.打乱列表 C.返回最大值 D.返回最小值",
        "answer": "A", "difficulty": 3,
        "explanation": "random.choice 从序列里随机选一个～每次结果不确定。做抽奖、抽卡游戏常用。shuffle 是打乱，max/min 不是 random 的功能！",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "math与random",
        "q_type": "judge",
        "content": "random.shuffle(a) 会原地打乱列表 a，返回 None。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！shuffle 原地打乱，不返回新列表～要保留原顺序先 copy 再 shuffle。做洗牌游戏常用，记住它是原地操作！",
    },

    # =============== L5 · time模块（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "time模块",
        "q_type": "single",
        "content": "import time，time.sleep(2) 的作用是？\nA.暂停 2 秒 B.暂停 2 毫秒 C.获取当前时间 D.计时 2 秒",
        "answer": "A", "difficulty": 2,
        "explanation": "time.sleep(2) 让程序暂停 2 秒～做倒计时、动画、限速常用。参数是秒，想暂停 0.5 秒用 sleep(0.5)。",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "time模块",
        "q_type": "single",
        "content": "import time，time.time() 返回什么？\nA.当前时间戳（从1970年1月1日开始的秒数，浮点数） B.当前日期字符串 C.当前小时 D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "time.time() 返回「时间戳」～从 1970-01-01 00:00:00 到现在的秒数（浮点）。常用算程序耗时：start=time.time() ... print(time.time()-start)。",
    },
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "time模块",
        "q_type": "judge",
        "content": "可以用 time.time() 在代码前后各取一次，相减算出代码运行耗时。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！start=time.time() 记开始，end=time.time() 记结束，end-start 就是耗时～这是最简单的计时方法，测算法效率常用！",
    },

    # =============== L5 · 综合应用（1 单选 + 0 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l5", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "用一行代码生成 1 到 10 所有偶数的平方列表，哪个对？\nA.[x**2 for x in range(1,11) if x%2==0] B.[x**2 for x in range(1,11) x%2==0] C.[if x%2==0 x**2 for x in range(1,11)] D.[x**2 if x%2==0 for x in range(1,11)]",
        "answer": "A", "difficulty": 4,
        "explanation": "推导式结构「表达式 for 变量 in 序列 if 条件」～A 正确：x**2 是表达式，for 遍历，if 筛偶数。结果 [4,16,36,64,100]，推导式综合应用！",
    },
]


# =========================================================================
# Python L6（27 题）：综合（数据库操作、面向对象）
# 知识点：类与对象 / 属性与方法 / 继承与多态 / SQLite数据库 / 数据库操作 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
PYTHON_L6_QUESTIONS = [
    # =============== L6 · 类与对象（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "类与对象",
        "q_type": "single",
        "content": "Python 用哪个关键字定义类？\nA.class B.def C.struct D.type",
        "answer": "A", "difficulty": 3,
        "explanation": "class 定义类～如 class Dog:。def 是定义函数，struct 是 C 语言的结构体，type 是查看类型。class 是面向对象的基础！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "类与对象",
        "q_type": "single",
        "content": "类和对象的关系是？\nA.类是模板，对象是按模板造出来的实物 B.对象是模板，类是实物 C.它俩一样 D.类包含对象",
        "answer": "A", "difficulty": 3,
        "explanation": "类是「设计图纸」，对象是按图纸造出来的「实物」～比如 Dog 类是图纸，dog1、dog2 是造出来的小狗。一个类能造很多对象！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "类与对象",
        "q_type": "single",
        "content": "class Dog: 里的 def __init__(self): 是什么？\nA.构造方法（创建对象时自动调用） B.普通方法 C.析构方法 D.静态方法",
        "answer": "A", "difficulty": 4,
        "explanation": "__init__ 是「构造方法」，创建对象时自动调用～用来初始化属性。self 指对象自己。__init__ 是面向对象最重要的方法！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "类与对象",
        "q_type": "judge",
        "content": "self 代表对象自己，调用方法时 Python 自动传入，不用手动传。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！self 是「对象自己」～dog.bark() 调用时，Python 自动把 dog 传给 self。定义方法要写 self，调用时不用传，Python 帮你传！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "类与对象",
        "q_type": "judge",
        "content": "一个类可以创建多个对象，每个对象的属性值可以不同。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！类是模板，能造很多对象～Dog 类造出 dog1（名字旺财）和 dog2（名字小黑），属性各自独立。这就是面向对象的灵活性！",
    },

    # =============== L6 · 属性与方法（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "single",
        "content": "在 __init__ 里怎么给对象设置属性 name？\nA.self.name = name B.name = name C.this.name = name D.obj.name = name",
        "answer": "A", "difficulty": 3,
        "explanation": "self.name = name 给对象设置属性～self 是对象自己，self.name 就是「这个对象的 name」。this 是 Java/JS，obj 是变量名不是关键字！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "single",
        "content": "dog = Dog('旺财') 创建对象，'旺财' 传给 __init__ 的哪个参数？\nA.name（第一个除 self 外的参数） B.self C.不传 D.报错",
        "answer": "A", "difficulty": 3,
        "explanation": "Dog('旺财') 调用 __init__(self, '旺财')～'旺财' 传给 name 参数（self 自动传 dog）。创建对象时传的参数给 __init__ 用！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "single",
        "content": "类里的「方法」其实就是？\nA.类里定义的函数 B.类里的变量 C.类外的函数 D.对象的属性",
        "answer": "A", "difficulty": 3,
        "explanation": "方法就是「类里的函数」～def bark(self): 是方法，跟普通函数区别是第一个参数是 self。调用时用 对象.方法名()！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "judge",
        "content": "对象.属性名 能访问对象的属性，如 dog.name 取出名字。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！点号 . 访问属性和方法～dog.name 取属性，dog.bark() 调方法。点号是面向对象的「成员访问」符，超常用！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "judge",
        "content": "对象能调用自己的方法，也能访问自己的属性。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！对象用自己的属性和方法都用点号～dog.name（属性）、dog.bark()（方法）。对象是「有属性有方法」的实体！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "属性与方法",
        "q_type": "program", "program_lang": "python",
        "content": "定义一个 Dog 类，有 name 属性（在 __init__ 里设置）和 bark 方法（输出 'Woof' 加名字）。读入一个名字，创建 Dog 对象并调用 bark。\n输入：一个名字（字符串）。\n输出：Woof + 名字（如输入 Tom，输出 WoofTom）。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "class Dog: def __init__(self, name): self.name = name; def bark(self): print('Woof'+self.name) → d = Dog(input()) → d.bark()～类+构造方法+方法，面向对象入门题！",
        "grading_rules": _py_grading([
            {"input": "Tom\n", "expected": "WoofTom\n", "hint": "输出 Woof+名字"},
            {"input": "Buddy\n", "expected": "WoofBuddy\n", "hint": "输出 Woof+名字"},
        ]),
    },

    # =============== L6 · 继承与多态（3 单选 + 2 判断 + 1 编程） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "single",
        "content": "class Cat(Animal): 表示什么？\nA.Cat 继承 Animal（Cat 是子类，Animal 是父类） B.Animal 继承 Cat C.它俩无关 D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "class 子类(父类): 表示继承～Cat 继承 Animal，Cat 能用 Animal 的属性和方法，还能加自己的。继承让代码复用，OOP 核心！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "single",
        "content": "子类想调用父类的 __init__ 方法，用哪个？\nA.super().__init__() B.parent().__init__() C.Animal.__init__() D.this.__init__()",
        "answer": "A", "difficulty": 4,
        "explanation": "super().__init__() 调用父类的构造方法～super() 返回父类对象。这能复用父类的初始化代码，继承时常用！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "single",
        "content": "「多态」是指？\nA.不同对象调用同名方法，表现出不同行为 B.一个方法多个名字 C.方法能改 D.属性能变",
        "answer": "A", "difficulty": 4,
        "explanation": "多态是「同名方法，不同行为」～Cat 和 Dog 都有 speak()，但 Cat 喵喵、Dog 汪汪。调用时不用管具体类型，自动表现对应行为！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "judge",
        "content": "子类能继承父类的所有方法和属性（除了私有的）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！子类自动拥有父类的方法和属性～不用重写就能用。还能加自己的新方法，或覆盖（重写）父类方法。继承=复用+扩展！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "judge",
        "content": "子类可以重写（覆盖）父类的方法，即定义同名方法替换父类的。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！子类定义和父类同名的方法，会「覆盖」父类的～调用时执行子类的版本。这叫「方法重写」，是多态的基础！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "继承与多态",
        "q_type": "program", "program_lang": "python",
        "content": "定义 Animal 父类有 speak 方法输出 'sound'，定义 Dog 子类重写 speak 输出 'Woof'。创建 Dog 对象调用 speak，输出结果。\n输入：无。\n输出：Woof。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "class Animal: def speak(self): print('sound') → class Dog(Animal): def speak(self): print('Woof') → Dog().speak()～子类重写父类方法，多态入门！",
        "grading_rules": _py_grading([
            {"input": "\n", "expected": "Woof\n", "hint": "重写后输出 Woof"},
        ]),
    },

    # =============== L6 · SQLite数据库（3 单选 + 2 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "SQLite数据库",
        "q_type": "single",
        "content": "Python 用哪个模块操作 SQLite 数据库？\nA.sqlite3 B.mysql C.psql D.sqlite",
        "answer": "A", "difficulty": 3,
        "explanation": "sqlite3 是 Python 内置的 SQLite 模块～import sqlite3 就能用。MySQL 要装第三方库。SQLite 是轻量级文件数据库，不用装服务器！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "SQLite数据库",
        "q_type": "single",
        "content": "连接数据库用哪个函数？\nA.sqlite3.connect() B.sqlite3.open() C.sqlite3.link() D.sqlite3.db()",
        "answer": "A", "difficulty": 3,
        "explanation": "sqlite3.connect('test.db') 连接数据库～不存在会自动创建。返回连接对象 conn，然后用 conn.cursor() 创建游标执行 SQL！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "SQLite数据库",
        "q_type": "single",
        "content": "执行 SQL 语句用什么？\nA.cursor.execute() B.conn.run() C.db.exec() D.sql.do()",
        "answer": "A", "difficulty": 3,
        "explanation": "cursor.execute('SELECT * FROM users') 执行 SQL～cursor 是游标对象，由 conn.cursor() 创建。execute 后用 fetchall() 取结果！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "SQLite数据库",
        "q_type": "judge",
        "content": "执行 INSERT/UPDATE/DELETE 后要 conn.commit() 才真正保存到数据库。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！增删改要 commit 提交才生效～不然只在内存没存盘。查询(SELECT)不用 commit。忘了 commit 数据就丢了，超重要！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "SQLite数据库",
        "q_type": "judge",
        "content": "用完数据库要 conn.close() 关闭连接，释放资源。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！用完要 close 关闭连接～不然占资源。推荐用 with 语句自动关闭，或 try-finally 确保 close。好习惯！",
    },

    # =============== L6 · 数据库操作（2 单选 + 1 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "数据库操作",
        "q_type": "single",
        "content": "查询数据后，fetchall() 返回什么？\nA.所有结果行（列表，每行是元组） B.一行 C.列名 D.整数",
        "answer": "A", "difficulty": 4,
        "explanation": "fetchall() 返回所有行，是个列表，每行是元组～如 [(1,'Tom'), (2,'Jerry')]。fetchone() 只返回一行。查询结果取数据用这俩！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "数据库操作",
        "q_type": "single",
        "content": "防止 SQL 注入，execute 传参数应该用？\nA.占位符 ?（如 execute('WHERE id=?', (1,))） B.字符串拼接 C.% 格式化 D.+ 拼接",
        "answer": "A", "difficulty": 4,
        "explanation": "用 ? 占位符 + 参数元组防注入～execute('SELECT * WHERE id=?', (1,))。字符串拼接/格式化会被注入攻击，超危险！安全第一！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "数据库操作",
        "q_type": "judge",
        "content": "SQL 语句里用 ? 占位符比字符串拼接更安全，能防止 SQL 注入攻击。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！? 占位符让数据库自动处理特殊字符，防注入～字符串拼接会把用户输入当代码执行，超危险。永远用占位符，别拼接！",
    },

    # =============== L6 · 综合应用（1 单选 + 1 判断 + 0 编程） ===============
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面代码输出什么？\n  class Counter:\n      def __init__(self):\n          self.count = 0\n      def add(self):\n          self.count += 1\n  c = Counter()\n  c.add()\n  c.add()\n  print(c.count)\nA.2 B.1 C.0 D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "c = Counter() 创建对象，count 初始 0～c.add() 两次后 count=2。print 输出 2。类+属性+方法+对象操作，OOP 综合应用！",
    },
    {
        "syllabus_version": "python-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "面向对象编程（OOP）的核心思想是「把数据和操作数据的方法打包成对象」。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！OOP 把「数据」（属性）和「操作」（方法）打包成对象～Dog 对象有 name 属性和 bark 方法。比面向过程更清晰，适合大项目！",
    },
]


# =========================================================================
# 汇总：所有 Python 题目（6 级 × 27 题 = 162 题）
# =========================================================================
ALL_PYTHON_QUESTIONS = (
    PYTHON_L1_QUESTIONS
    + PYTHON_L2_QUESTIONS
    + PYTHON_L3_QUESTIONS
    + PYTHON_L4_QUESTIONS
    + PYTHON_L5_QUESTIONS
    + PYTHON_L6_QUESTIONS
)


# =========================================================================
# 各级题目列表映射（方便按级别取用）
# =========================================================================
PYTHON_QUESTIONS_BY_LEVEL = {
    "python-l1": PYTHON_L1_QUESTIONS,
    "python-l2": PYTHON_L2_QUESTIONS,
    "python-l3": PYTHON_L3_QUESTIONS,
    "python-l4": PYTHON_L4_QUESTIONS,
    "python-l5": PYTHON_L5_QUESTIONS,
    "python-l6": PYTHON_L6_QUESTIONS,
}


def _verify():
    """自检：题目总数、各级数量、题型分布。"""
    total = len(ALL_PYTHON_QUESTIONS)
    print(f"总题数: {total}（应为 162）")
    assert total == 162, f"题目总数不对: {total} != 162"

    from collections import Counter

    by_level = Counter(q["syllabus_version"] for q in ALL_PYTHON_QUESTIONS)
    print("\n各级题数:")
    for lv in range(1, 7):
        key = f"python-l{lv}"
        cnt = by_level[key]
        print(f"  {key}: {cnt} 题（应为 27）")
        assert cnt == 27, f"{key} 题数不对: {cnt} != 27"

    print("\n各级题型分布:")
    for lv in range(1, 7):
        key = f"python-l{lv}"
        qs = PYTHON_QUESTIONS_BY_LEVEL[key]
        dist = Counter(q["q_type"] for q in qs)
        print(
            f"  {key}: 单选 {dist['single']} + 判断 {dist['judge']} "
            f"+ 编程 {dist['program']} = {sum(dist.values())}"
        )
        assert dist["single"] == 15, f"{key} 单选题数不对: {dist['single']} != 15"
        assert dist["judge"] == 10, f"{key} 判断题数不对: {dist['judge']} != 10"
        assert dist["program"] == 2, f"{key} 编程题数不对: {dist['program']} != 2"

    # 字段完整性
    required_fields = {
        "single": {"syllabus_version", "grade_level", "knowledge_point", "q_type", "content", "answer", "difficulty", "explanation"},
        "judge": {"syllabus_version", "grade_level", "knowledge_point", "q_type", "content", "answer", "difficulty", "explanation"},
        "program": {"syllabus_version", "grade_level", "knowledge_point", "q_type", "content", "answer", "difficulty", "explanation", "program_lang", "grading_rules"},
    }
    print("\n字段完整性检查:")
    for q in ALL_PYTHON_QUESTIONS:
        need = required_fields[q["q_type"]]
        missing = need - set(q.keys())
        assert not missing, f"题目缺字段 {missing}: {q['content'][:30]}..."
        # program 题必须有 program_lang=python
        if q["q_type"] == "program":
            assert q["program_lang"] == "python", f"编程题 program_lang 不是 python: {q['content'][:30]}"
    print("  全部题目字段完整 ✓")

    # 各级知识点覆盖
    print("\n各级知识点:")
    for lv in range(1, 7):
        key = f"python-l{lv}"
        kps = []
        for q in PYTHON_QUESTIONS_BY_LEVEL[key]:
            if q["knowledge_point"] not in kps:
                kps.append(q["knowledge_point"])
        print(f"  {key}: {' / '.join(kps)}")

    print("\n[verify] 全部检查通过 ✓")


if __name__ == "__main__":
    _verify()
