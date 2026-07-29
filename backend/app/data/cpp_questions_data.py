"""C++ 1-8 级题库数据（按电子学会 / GESP C++ 考纲）。

共 8 级 × 27 题 = 216 题
每级题型分布：15 单选(single) + 10 判断(judge) + 2 编程(program)

考纲对齐（电子学会青少年软件编程 C/C++ 等级考试标准 2025 修订版 + GESP C++ 1-8 级）：
- L1（3-4 年级·入门启蒙）：顺序结构与程序框架 / 变量与数据类型 / 输入输出 cin&cout / 算术运算 / 关系运算 / 综合应用
- L2（4-5 年级·基础进阶）：分支结构 if / if-else 语句 / 逻辑运算 / char 数组字符串 / 循环概念入门 / 综合应用
- L3（5-6 年级·循环入门）：for 循环 / while 循环 / 循环控制 break&continue / 一维数组 / 循环嵌套 / 综合应用
- L4（6-7 年级·数组与函数）：二维数组 / 函数定义与调用 / 值传递与作用域 / 递归入门 / 简单排序 / 顺序查找
- L5（7-8 年级·字符串与算法进阶）：C++ string 类 / 字符数组处理 / 插入与快速排序 / 二分查找 / 递归进阶 / 结构体
- L6（8-9 年级·数据结构与复杂算法）：栈 / 队列 / 单链表 / 贪心算法 / 动态规划入门 / 指针基础
- L7（高一·高级数据结构与算法）：STL 容器 / 二叉树遍历 / 动态规划进阶 / 图遍历 DFS&BFS / 指针进阶 / 综合应用
- L8（高二·综合算法与工程化）：面向对象基础 / 图论算法 / 复杂动态规划 / 二叉搜索树与堆 / 代码优化与工程化 / 综合应用

字段说明（对齐 backend/app/models/question.py）：
- syllabus_version: cpp-l1 ~ cpp-l8
- grade_level: 建议年级
- knowledge_point: 考纲知识点（原名，存储层用）
- q_type: single / judge / program
- content / answer / difficulty(1-5) / explanation
- program 题: program_lang="cpp", grading_rules 为 JSON 字符串
  grading_rules 格式: {"language":"cpp","time_limit":2,"memory_limit":128,
                       "test_cases":[{"input":"","expected":"...\\n","hint":"..."}]}

文案规范（对齐 AGENTS.md）：
- C++ 题目面对 3 年级~高三学生，必须保持技术术语准确（cin/cout/for/if 等不可替换）
- 解析用相对易懂的方式解释原理，低级别（L1-L3）语气更友好
"""
import json


def _cpp_grading(test_cases, time_limit=2, memory_limit=128):
    """生成 C++ 编程题 grading_rules JSON 字符串。

    Args:
        test_cases: [{"input":"...", "expected":"...", "hint":"..."}, ...]
        time_limit: 秒
        memory_limit: MB
    """
    return json.dumps(
        {
            "language": "cpp",
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            "test_cases": test_cases,
        },
        ensure_ascii=False,
    )


# =========================================================================
# C++ L1（27 题）：入门启蒙
# 知识点：顺序结构与程序框架 / 变量与数据类型 / 输入输出 cin&cout /
#        算术运算 / 关系运算 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L1_QUESTIONS = [
    # =============== L1 · 顺序结构与程序框架（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "顺序结构与程序框架",
        "q_type": "single",
        "content": "一个最简单的 C++ 程序里，程序从哪个函数开始执行？A.main B.start C.begin D.run",
        "answer": "A", "difficulty": 1,
        "explanation": "C++ 程序总是从 main 函数开始跑，就像上课铃响了先走进教室一样～start/begin/run 都不是 C++ 的入口函数哦。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "顺序结构与程序框架",
        "q_type": "single",
        "content": "下面哪行是正确的 C++ 程序开头？A.#include <iostream> B.#include iostream C.import iostream D.include(iostream)",
        "answer": "A", "difficulty": 1,
        "explanation": "C++ 用 #include <iostream> 把输入输出工具箱搬进来，尖括号 <> 里写头文件名字～import 是 Python 的写法，少了 # 或少括号都不对。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "顺序结构与程序框架",
        "q_type": "single",
        "content": "using namespace std; 这句话的作用是？A.使用标准命名空间，省得每次写 std:: B.定义变量 C.结束程序 D.打印输出",
        "answer": "A", "difficulty": 2,
        "explanation": "std 是「标准」的缩写，写了这句话后 cout、cin 就不用写 std::cout 啦，少打几个字～它不定义变量也不结束程序。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "顺序结构与程序框架",
        "q_type": "judge",
        "content": "每条 C++ 语句结束都要加分号 ;",
        "answer": "true", "difficulty": 1,
        "explanation": "对！分号就像句号，告诉电脑「这句话说完了」～漏了分号是新手最常见的错误，编译器会报错哦。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "顺序结构与程序框架",
        "q_type": "judge",
        "content": "main 函数的括号里 return 0; 表示程序正常结束。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！return 0; 告诉操作系统「我跑完了，没出问题」～返回 0 表示正常，非 0 通常表示有错误。",
    },

    # =============== L1 · 变量与数据类型（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "想存一个整数（比如年龄 10），该用哪种数据类型？A.int B.double C.char D.string",
        "answer": "A", "difficulty": 1,
        "explanation": "int 专门存整数（integer 的缩写）～double 存小数，char 存单个字符，string 存一串文字，存年龄当然用 int！",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "下面哪个是合法的变量名？A.score B.2score C.score! D.int",
        "answer": "A", "difficulty": 2,
        "explanation": "变量名只能用字母、数字、下划线，且不能数字开头、不能用关键字～score 合法；2score 数字开头不行；score! 有特殊符号；int 是关键字不能当名字。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "single",
        "content": "double 类型用来存什么？A.小数（带小数点的数） B.整数 C.单个字符 D.真或假",
        "answer": "A", "difficulty": 1,
        "explanation": "double 存带小数点的数，比如 3.14、0.5～存整数用 int，存字符用 char，存真假用 bool。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "变量与数据类型",
        "q_type": "judge",
        "content": "int a = 5; 这句话做了两件事：定义变量 a，并给它赋值 5。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！int a = 5; 就是「申请一个装整数的小盒子叫 a，里面放上 5」～定义和赋值一起完成，超方便！",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "变量与数据类型",
        "q_type": "judge",
        "content": "char c = 'A'; 这样写是错的，因为 char 只能存数字。",
        "answer": "false", "difficulty": 2,
        "explanation": "错啦！char 就是专门存单个字符的，'A'、'B'、'9'、'?' 都能存～用单引号包起来一个字符就行，char 不只能存数字哦。",
    },

    # =============== L1 · 输入输出 cin&cout（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "输入输出 cin&cout",
        "q_type": "single",
        "content": "想在屏幕上打印「Hello」，正确的写法是？A.cout << \"Hello\"; B.cin >> \"Hello\"; C.print(\"Hello\"); D.cout >> \"Hello\";",
        "answer": "A", "difficulty": 1,
        "explanation": "cout 是「屏幕输出」，用 << 把内容送到屏幕上～cin 是输入用 >>，print 是 Python 的写法，cout >> 方向反了都不对。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "输入输出 cin&cout",
        "q_type": "single",
        "content": "想从键盘读入一个整数存到变量 n 里，正确写法是？A.cin >> n; B.cin << n; C.cout >> n; D.input(n);",
        "answer": "A", "difficulty": 2,
        "explanation": "cin 是「键盘输入」，用 >> 把键盘敲的数据送到变量里～cout 是输出用 <<，方向要分清：cin >> 收进来，cout << 送出去！",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "输入输出 cin&cout",
        "q_type": "single",
        "content": "cout << endl; 的作用是？A.换行 B.结束程序 C.清空屏幕 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "endl 是「end line」换行的意思，相当于敲个回车～也可以用 \\n 换行。它不结束程序也不清屏哦。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "输入输出 cin&cout",
        "q_type": "judge",
        "content": "cout 可以一次性输出多个内容，比如 cout << \"a=\" << a;",
        "answer": "true", "difficulty": 2,
        "explanation": "对！用多个 << 串起来就行～cout << \"a=\" << a; 会先打印 a= 再打印变量 a 的值，像「a=5」这样。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "输入输出 cin&cout",
        "q_type": "judge",
        "content": "使用 cin 和 cout 必须先 #include <iostream>。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！cin/cout 住在 iostream 这个工具箱里，不搬进来就用不了～就像不打开工具箱拿不到里面的锤子一样。",
    },

    # =============== L1 · 算术运算（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "算术运算",
        "q_type": "single",
        "content": "7 % 3 的结果是？A.1 B.2 C.0 D.3",
        "answer": "A", "difficulty": 2,
        "explanation": "% 是取余数（求余）运算～7 除以 3 商 2 余 1，所以 7 % 3 = 1。想判断奇偶数经常用它：n % 2 == 1 是奇数。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "算术运算",
        "q_type": "single",
        "content": "在 C++ 里，7 / 2 的结果是？A.3 B.3.5 C.4 D.2",
        "answer": "A", "difficulty": 2,
        "explanation": "注意！两个整数相除，结果还是整数（直接去掉小数部分）～7/2 = 3 而不是 3.5。想要 3.5 得让其中一个是 double，比如 7.0/2。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "算术运算",
        "q_type": "single",
        "content": "想计算 2 的 3 次方（2×2×2），下面哪个写法对？A.2*2*2 B.2^3 C.2**3 D.pow(2,3)（需包含 cmath）",
        "answer": "A", "difficulty": 2,
        "explanation": "C++ 里 ^ 是「按位异或」不是乘方！直接算 2*2*2 最稳～或者用 pow(2,3)（要 #include <cmath>）。2**3 是 Python 写法。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 3, "knowledge_point": "算术运算",
        "q_type": "judge",
        "content": "+、-、*、/ 分别表示加、减、乘、除。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！这四个是最基本的算术运算符～注意乘是 *（星号）不是 ×，除是 /（斜杠）不是 ÷，电脑键盘上就这几个符号。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "算术运算",
        "q_type": "judge",
        "content": "10 / 0 在 C++ 里能正常算出结果。",
        "answer": "false", "difficulty": 2,
        "explanation": "错！除以 0 是不允许的，会导致程序崩溃或报错～就像把 10 块饼干分给 0 个人，没法分嘛！写代码要避免除以 0。",
    },

    # =============== L1 · 关系运算（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "关系运算",
        "q_type": "single",
        "content": "判断两个数是否相等，用哪个运算符？A.== B.= C.!= D.>=",
        "answer": "A", "difficulty": 2,
        "explanation": "== 是「判断相等」，= 是「赋值」～这是新手最容易搞混的！a == 5 是问 a 等不等于 5，a = 5 是把 5 塞给 a。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "关系运算",
        "q_type": "single",
        "content": "5 > 3 这个表达式的结果是？A.true（真） B.false（假） C.5 D.3",
        "answer": "A", "difficulty": 2,
        "explanation": "5 确实大于 3，所以 5 > 3 成立，结果是 true（真）～关系运算的结果只有 true 或 false 两种，不是数字哦。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "关系运算",
        "q_type": "judge",
        "content": "!= 表示「不等于」。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！!= 就是「不相等」～a != 5 意思是 a 不等于 5。感叹号 ! 在 C++ 里常表示「否定」。",
    },

    # =============== L1 · 综合应用（1 单选 + 1 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面程序输出什么？\\n  int a = 3, b = 5;\\n  cout << a + b;\\nA.8 B.35 C.3+5 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "a 存 3，b 存 5，a + b = 8，cout 把 8 打印出来～不是拼成 35（那是字符串拼接才会），也不是打印 3+5 这几个字符。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "顺序结构程序按从上到下的顺序一条一条执行语句。",
        "answer": "true", "difficulty": 1,
        "explanation": "对！顺序结构就像排队做事，先来后到，从上往下一句句跑～这是最基础的程序结构，后面才会学分支和循环。",
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "请写一个完整 C++ 程序：在屏幕上输出一行 Hello, World!（注意末尾换行）。",
        "answer": "see_grading_rules", "difficulty": 1,
        "explanation": "这是 C++ 的「入门第一课」！#include <iostream> 搬工具箱 → using namespace std; → main 函数里 cout << \"Hello, World!\" << endl; → return 0; 就搞定啦～",
        "grading_rules": _cpp_grading([
            {"input": "", "expected": "Hello, World!\n", "hint": "无输入，输出 Hello, World! 并换行"},
        ]),
    },
    {
        "syllabus_version": "cpp-l1", "grade_level": 4, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入两个整数 a 和 b，输出它们的和。\\n输入格式：一行两个整数，用空格隔开。\\n输出格式：一个整数，表示 a+b 的结果。",
        "answer": "see_grading_rules", "difficulty": 2,
        "explanation": "cin >> a >> b; 一次读两个数（空格隔开），cout << a + b; 输出和～核心就这两句，套上 main 框架就行！",
        "grading_rules": _cpp_grading([
            {"input": "3 5\n", "expected": "8\n", "hint": "3+5=8"},
            {"input": "10 20\n", "expected": "30\n", "hint": "10+20=30"},
            {"input": "-1 1\n", "expected": "0\n", "hint": "负数加正数"},
        ]),
    },
]

# =========================================================================
# C++ L2（27 题）：基础进阶
# 知识点：分支结构 if / if-else 语句 / 逻辑运算 / char 数组字符串 /
#        循环概念入门 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L2_QUESTIONS = [
    # =============== L2 · 分支结构 if（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "分支结构 if",
        "q_type": "single",
        "content": "if 语句的格式是？A.if (条件) { 语句 } B.if 条件 then 语句 C.if [条件] 语句 D.if <条件> 语句",
        "answer": "A", "difficulty": 2,
        "explanation": "C++ 的 if 把条件放在小括号 () 里，要执行的语句放在花括号 {} 里～if...then 是其他语言的写法，方括号尖括号都不对。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "分支结构 if",
        "q_type": "single",
        "content": "if (a > 0) cout << \"正数\";  如果 a = -5，会输出什么？A.什么都不输出 B.正数 C.负数 D.报错",
        "answer": "A", "difficulty": 2,
        "explanation": "a = -5 不满足 a > 0，所以花括号里的语句不执行，什么都不会打印～if 只在条件成立时才做事。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "分支结构 if",
        "q_type": "single",
        "content": "下面哪种情况适合用 if 语句？A.判断分数是否及格再决定显示什么 B.重复做 10 次加法 C.存 100 个数 D.定义一个函数",
        "answer": "A", "difficulty": 2,
        "explanation": "if 是「看条件做决定」的分支结构，判断及格/不及格正合适～重复做事用循环，存一堆数用数组，封装代码用函数。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "分支结构 if",
        "q_type": "judge",
        "content": "if 后面的条件要用小括号 () 括起来。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！if (条件) 是固定格式，小括号不能省～漏了括号编译器会报错，这是 C++ 的硬规矩。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "分支结构 if",
        "q_type": "judge",
        "content": "if (a > b && a > c) 表示「a 大于 b 且 a 大于 c」。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！&& 是「并且」的意思，两个条件都要满足才成立～这个条件常用来判断 a 是不是三个数里最大的。",
    },

    # =============== L2 · if-else 语句（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "if-else 语句",
        "q_type": "single",
        "content": "if-else 语句的作用是？A.条件成立做一件事，不成立做另一件事 B.重复做某件事 C.定义变量 D.结束程序",
        "answer": "A", "difficulty": 2,
        "explanation": "if-else 就是「如果…就…否则…」～条件真做 if 部分，条件假做 else 部分，二选一。重复做事用循环。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "if-else 语句",
        "q_type": "single",
        "content": "判断奇偶数：如果 n % 2 == 0 是偶数，否则是奇数。下面哪个写法对？A.if (n%2==0) cout<<\"偶数\"; else cout<<\"奇数\"; B.if n%2==0 cout<<\"偶数\" else cout<<\"奇数\" C.if (n%2==0) { cout<<\"偶数\" } else { cout<<\"奇数\" }（少了分号） D.else cout<<\"偶数\"; if (n%2==0) cout<<\"奇数\";",
        "answer": "A", "difficulty": 3,
        "explanation": "A 完整正确：if 判断条件，else 处理其他情况～B 漏了括号；C 花括号里少了分号；D 顺序反了逻辑错。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "if-else 语句",
        "q_type": "single",
        "content": "判断闰年的规则：能被 4 整除但不能被 100 整除，或者能被 400 整除。下面哪个条件对？A.(y%4==0 && y%100!=0) || (y%400==0) B.(y%4==0 || y%100!=0) && (y%400==0) C.y%4==0 D.y%400==0",
        "answer": "A", "difficulty": 3,
        "explanation": "闰年有两种情况，用 ||（或）连起来：①能被 4 整除且不能被 100 整除 ②能被 400 整除～只判断 y%4==0 会多算，只判断 y%400==0 会漏算。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "if-else 语句",
        "q_type": "judge",
        "content": "if-else 语句中，else 部分可以省略，只保留 if。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！如果条件不成立时啥都不用做，就不用写 else～比如「如果是会员就打折」，不是会员就原价，啥都不用做就不用 else。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "if-else 语句",
        "q_type": "judge",
        "content": "if-else if-else 可以用来处理多种情况（比如成绩分优良中差）。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！if-else if-else 能串起来处理好多种情况～比如：>=90 优，>=80 良，>=60 中，else 差。一个 if 只能分两路，多路用它最合适。",
    },

    # =============== L2 · 逻辑运算（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "逻辑运算",
        "q_type": "single",
        "content": "&& 表示什么意思？A.逻辑与（并且） B.逻辑或（或者） C.逻辑非（取反） D.按位与",
        "answer": "A", "difficulty": 2,
        "explanation": "&& 是逻辑与，表示「两个条件都成立才算真」～比如「年龄>=6 && 年龄<=12」表示 6 到 12 岁。|| 是或，! 是非。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "逻辑运算",
        "q_type": "single",
        "content": "!(3 > 5) 的结果是？A.true B.false C.3 D.5",
        "answer": "A", "difficulty": 2,
        "explanation": "3 > 5 是 false，! 表示「取反」，false 取反就是 true～! 就像说「不」，把真假反过来。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "逻辑运算",
        "q_type": "single",
        "content": "判断「a 在 1 到 10 之间（含 1 和 10）」，正确写法是？A.a >= 1 && a <= 10 B.a >= 1 || a <= 10 C.1 <= a <= 10 D.a >= 1 and a <= 10",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ 要拆成两个条件用 && 连～a>=1 || a<=10 几乎对所有数都成立（或）；1<=a<=10 在 C++ 里会先算 1<=a 得 0/1 再和 10 比，逻辑错；and 是 Python 写法。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 4, "knowledge_point": "逻辑运算",
        "q_type": "judge",
        "content": "|| 表示「或者」，两个条件只要有一个成立结果就是 true。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！|| 是逻辑或，左边右边有一个真就是真～比如「周末 || 节假日」只要有一个成立就不用上学。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "逻辑运算",
        "q_type": "judge",
        "content": "true && false 的结果是 true。",
        "answer": "false", "difficulty": 2,
        "explanation": "错！&& 是「并且」，两个都得真才是真～true && false 有一个是 false，结果就是 false。只有 true && true 才是 true。",
    },

    # =============== L2 · char 数组字符串（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "char 数组字符串",
        "q_type": "single",
        "content": "在 C++ 里，用 char 数组存字符串 \"hello\"，数组至少要多大？A.6（5 个字母 + 1 个结束符） B.5 C.4 D.10",
        "answer": "A", "difficulty": 3,
        "explanation": "C 风格字符串末尾要藏一个 '\\0'（空字符）当结束标记～\"hello\" 5 个字母 + 1 个 \\0 = 6，数组至少要 6 个位置。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "char 数组字符串",
        "q_type": "single",
        "content": "想计算 char 数组 s 里字符串的长度，用哪个函数？A.strlen(s) B.length(s) C.size(s) D.len(s)",
        "answer": "A", "difficulty": 3,
        "explanation": "char 数组（C 风格字符串）求长度用 strlen(s)～length/size/len 是其他类型的写法。注意 strlen 不算末尾的 \\0。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "char 数组字符串",
        "q_type": "single",
        "content": "char s[10] = \"cat\"; 那 s[0] 是什么？A.'c' B.\"cat\" C.'C' D.3",
        "answer": "A", "difficulty": 2,
        "explanation": "s[0] 是数组第 0 个位置，存的是第一个字符 'c'（小写、单引号）～s 整体才是 \"cat\"，s[0] 只是其中一个字符。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "char 数组字符串",
        "q_type": "judge",
        "content": "char 数组里的字符串用 '\\0' 作为结束标志。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！C 风格字符串靠 \\0 判断「字符串到这里结束」～所以 strlen 算长度遇到 \\0 就停，不算它本身。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "char 数组字符串",
        "q_type": "judge",
        "content": "可以用 cin >> s; 直接读入一个 char 数组 s（无空格的字符串）。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！cin >> s; 能读入一个不含空格的字符串到 char 数组～但要注意数组别越界，且 cin 遇到空格就停，含空格要用 cin.getline。",
    },

    # =============== L2 · 循环概念入门（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "循环概念入门",
        "q_type": "single",
        "content": "「循环」结构最适合做什么？A.重复做某件事很多次 B.做选择 C.定义变量 D.结束程序",
        "answer": "A", "difficulty": 2,
        "explanation": "循环就是「重复做」～比如打印 1 到 100、算 10 个数的和，不用写 100 行，用循环几行搞定！做选择用 if，定义变量用类型名。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "循环概念入门",
        "q_type": "single",
        "content": "下面哪个是 C++ 的循环语句？（只选 L2 阶段了解概念即可）A.for / while B.if / else C.cin / cout D.int / double",
        "answer": "A", "difficulty": 2,
        "explanation": "C++ 的循环主要有 for 和 while 两种～if/else 是分支，cin/cout 是输入输出，int/double 是数据类型，都不是循环。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "循环概念入门",
        "q_type": "judge",
        "content": "循环的作用是让一段代码重复执行，避免重复写很多遍相同的代码。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！循环是「偷懒神器」～要打印 100 次「你好」，不用写 100 行 cout，用循环几行就搞定，还不会写错。",
    },

    # =============== L2 · 综合应用（1 单选 + 1 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面程序输入 7，输出什么？\\n  int n; cin >> n;\\n  if (n % 2 == 0) cout << \"even\";\\n  else cout << \"odd\";\\nA.odd B.even C.7 D.什么都不输出",
        "answer": "A", "difficulty": 3,
        "explanation": "n=7，7%2=1 不等于 0，所以走 else 分支，输出 odd（奇数）～if 判断偶数，else 处理奇数，逻辑清晰。",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "分支结构让程序能根据不同情况做不同的事，不再只会一条路走到底。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！分支结构（if/if-else）让程序有了「判断」能力～就像走到岔路口能选走哪条，而不是只能直走。这是程序变聪明的第一步！",
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入一个整数 n，判断它是正数、负数还是零，并输出对应的文字。\\n输入：一个整数 n。\\n输出：如果 n>0 输出 positive；n<0 输出 negative；n==0 输出 zero。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "用 if-else if-else 三路判断：if(n>0) 输出 positive；else if(n<0) 输出 negative；else 输出 zero。注意 0 要单独处理，不能漏！",
        "grading_rules": _cpp_grading([
            {"input": "5\n", "expected": "positive\n", "hint": "正数"},
            {"input": "-3\n", "expected": "negative\n", "hint": "负数"},
            {"input": "0\n", "expected": "zero\n", "hint": "零"},
        ]),
    },
    {
        "syllabus_version": "cpp-l2", "grade_level": 5, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入一个年份 y，判断是不是闰年，是则输出 yes，不是输出 no。\\n闰年规则：能被 4 整除且不能被 100 整除，或者能被 400 整除。\\n输入：一个整数 y。\\n输出：yes 或 no。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "条件：(y%4==0 && y%100!=0) || (y%400==0)～2000 能被 400 整除是闰年，1900 能被 100 整除但不能被 400 整除不是闰年，2024 能被 4 整除不被 100 整除是闰年。",
        "grading_rules": _cpp_grading([
            {"input": "2000\n", "expected": "yes\n", "hint": "能被400整除是闰年"},
            {"input": "1900\n", "expected": "no\n", "hint": "能被100但不能被400不是闰年"},
            {"input": "2024\n", "expected": "yes\n", "hint": "能被4不被100是闰年"},
            {"input": "2023\n", "expected": "no\n", "hint": "普通非闰年"},
        ]),
    },
]

# =========================================================================
# C++ L3（27 题）：循环入门
# 知识点：for 循环 / while 循环 / 循环控制 break&continue / 一维数组 /
#        循环嵌套 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L3_QUESTIONS = [
    # =============== L3 · for 循环（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 5, "knowledge_point": "for 循环",
        "q_type": "single",
        "content": "for (int i = 1; i <= 5; i++) 这个循环执行几次？A.5 次 B.4 次 C.6 次 D.无限次",
        "answer": "A", "difficulty": 2,
        "explanation": "i 从 1 开始，每次 +1，到 5 还执行（含 5），所以是 1,2,3,4,5 共 5 次～i<=5 的等号别漏，漏了就只 4 次。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 5, "knowledge_point": "for 循环",
        "q_type": "single",
        "content": "for 循环的三部分（初始化; 条件; 更新）用什么东西隔开？A.分号 ; B.逗号 , C.冒号 : D.空格",
        "answer": "A", "difficulty": 2,
        "explanation": "for 的三部分用分号 ; 隔开：for (初始化; 条件; 更新)～逗号、冒号都不行，这是固定语法。注意是隔开不是结束语句。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "for 循环",
        "q_type": "single",
        "content": "下面哪个 for 循环能打印 0 到 9（含 0 和 9）？A.for(int i=0; i<10; i++) cout<<i; B.for(int i=0; i<=10; i++) cout<<i; C.for(int i=1; i<10; i++) cout<<i; D.for(int i=0; i<9; i++) cout<<i;",
        "answer": "A", "difficulty": 3,
        "explanation": "0 到 9 共 10 个数：i 从 0 开始，i<10 时执行（最后 i=9 执行完变 10 退出）～B 会到 10，C 从 1 开始漏了 0，D 到 8 漏了 9。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 5, "knowledge_point": "for 循环",
        "q_type": "judge",
        "content": "for 循环里 i++ 和 i = i + 1 效果一样，都是让 i 加 1。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！i++ 是 i=i+1 的简写，更省事～还有 ++i、i+=1 都一样。这是 C++ 的常用简写，让代码更简洁。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "for 循环",
        "q_type": "judge",
        "content": "for (int i = 0; i < 0; i++) 这个循环一次都不执行。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！i=0，条件 i<0 一开始就 false，所以循环体一次都不跑～循环开始前会先检查条件，条件假就直接跳过。",
    },

    # =============== L3 · while 循环（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 5, "knowledge_point": "while 循环",
        "q_type": "single",
        "content": "while 循环的特点是？A.先判断条件，再决定要不要执行循环体 B.先执行一次再判断 C.固定次数循环 D.不判断条件",
        "answer": "A", "difficulty": 2,
        "explanation": "while 是「当…就…」，先看条件成不成立，成立才执行～条件一开始就假，循环体一次都不跑。do-while 才是先执行再判断。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "while 循环",
        "q_type": "single",
        "content": "下面代码输出什么？\\n  int i = 1;\\n  while (i <= 3) { cout << i << \" \"; i++; }\\nA.1 2 3  B.1 2 3 4  C.0 1 2  D.2 3 4",
        "answer": "A", "difficulty": 3,
        "explanation": "i=1<=3 打印 1，i 变 2；2<=3 打印 2，i 变 3；3<=3 打印 3，i 变 4；4<=3 假退出～输出 1 2 3，别忘了 i++ 让 i 长大，不然死循环！",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "while 循环",
        "q_type": "single",
        "content": "用 while 循环时，最容易犯的错误是？A.忘记更新循环变量导致死循环 B.忘记加分号 C.忘记写 main D.忘记 #include",
        "answer": "A", "difficulty": 3,
        "explanation": "while 循环体里必须更新循环变量（比如 i++），不然条件永远成立，程序会一直转停不下来（死循环）～for 把更新写在头部不容易忘。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 5, "knowledge_point": "while 循环",
        "q_type": "judge",
        "content": "while (true) 会一直循环，除非循环体里有 break 或程序被强制停止。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！true 永远为真，while(true) 是「死循环」～通常要在里面用 break 在合适时机跳出来，否则程序会卡住一直转。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "while 循环",
        "q_type": "judge",
        "content": "while 和 for 可以互相转换，能做的事基本一样。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！for 和 while 本质都是循环，能互相改写～for 适合固定次数（知道循环几次），while 适合不确定次数（看条件何时满足）。",
    },

    # =============== L3 · 循环控制 break&continue（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环控制 break&continue",
        "q_type": "single",
        "content": "break 语句的作用是？A.跳出当前循环 B.跳过本次循环剩下部分，进入下一次 C.结束程序 D.暂停程序",
        "answer": "A", "difficulty": 3,
        "explanation": "break 是「打破」循环，直接跳出整个循环不再继续～continue 是「跳过这一次」继续下一次，别搞混！",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环控制 break&continue",
        "q_type": "single",
        "content": "continue 语句的作用是？A.跳过本次循环剩余语句，直接进入下一次循环判断 B.跳出整个循环 C.重新开始程序 D.继续执行下一条语句",
        "answer": "A", "difficulty": 3,
        "explanation": "continue 是「这次不做了，直接下一轮」～它跳过本次剩下的代码，回到循环条件判断继续。break 才是跳出整个循环。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环控制 break&continue",
        "q_type": "single",
        "content": "下面程序输出什么？\\n  for (int i = 1; i <= 5; i++) {\\n    if (i == 3) continue;\\n    cout << i << \" \";\\n  }\\nA.1 2 4 5  B.1 2 3 4 5  C.1 2  D.3",
        "answer": "A", "difficulty": 3,
        "explanation": "i=3 时遇到 continue，跳过 cout，不打印 3，直接进下一轮～所以输出 1 2 4 5，正好少了 3。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环控制 break&continue",
        "q_type": "judge",
        "content": "break 只能跳出最内层的一层循环，不能一次跳出多层循环。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！break 只跳出它所在的那一层循环～要跳出多层得用标志变量配合，或者（L7+）用带标签的写法。嵌套循环里 break 只跳一层。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环控制 break&continue",
        "q_type": "judge",
        "content": "continue 和 break 一样，都会终止整个循环。",
        "answer": "false", "difficulty": 2,
        "explanation": "错！continue 只跳过这一次，循环还会继续；break 才是终止整个循环～它俩作用完全不同，continue 是「这一次算了」，break 是「不干了」。",
    },

    # =============== L3 · 一维数组（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "一维数组",
        "q_type": "single",
        "content": "定义一个能装 5 个整数的数组，正确写法是？A.int a[5]; B.int a(5); C.array a[5]; D.int[5] a;",
        "answer": "A", "difficulty": 2,
        "explanation": "C++ 定义数组：类型 名字[大小]～int a[5]; 就是「申请一个装 5 个 int 的小柜子叫 a」。其他写法语法都不对。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "一维数组",
        "q_type": "single",
        "content": "int a[5] = {1, 2, 3, 4, 5}; 那 a[2] 的值是？A.3 B.2 C.1 D.5",
        "answer": "A", "difficulty": 2,
        "explanation": "数组下标从 0 开始！a[0]=1, a[1]=2, a[2]=3, a[3]=4, a[4]=5～所以 a[2]=3。下标从 0 数是 C++ 的规矩，别从 1 数。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "一维数组",
        "q_type": "single",
        "content": "定义 int a[10]; 下面哪个访问是越界的（出错）？A.a[10] B.a[0] C.a[9] D.a[5]",
        "answer": "A", "difficulty": 3,
        "explanation": "大小 10 的数组，下标范围是 0~9～a[10] 越界（不存在），可能读到乱码或崩溃。a[0]~a[9] 都合法。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "一维数组",
        "q_type": "judge",
        "content": "数组的下标从 0 开始，最大下标是数组大小减 1。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！大小为 n 的数组，下标是 0 到 n-1～比如 a[5]，下标 0~4，没有 a[5]。这是新手最容易越界的地方，要记牢。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "一维数组",
        "q_type": "judge",
        "content": "可以用 for 循环配合数组下标来遍历（挨个访问）数组的每个元素。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！for(int i=0; i<n; i++) cout << a[i]; 是最常用的数组遍历套路～循环变量当数组下标，挨个访问，超方便。",
    },

    # =============== L3 · 循环嵌套（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环嵌套",
        "q_type": "single",
        "content": "外层循环 3 次，内层循环 4 次，内层循环体一共执行几次？A.12 次 B.7 次 C.3 次 D.4 次",
        "answer": "A", "difficulty": 3,
        "explanation": "外层每跑一次，内层跑完整一轮（4 次）～外层 3 次 × 内层 4 次 = 12 次。乘法关系，像九九乘法表那样。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环嵌套",
        "q_type": "single",
        "content": "打印九九乘法表，一般用什么结构？A.两层 for 循环嵌套 B.一层 for 循环 C.一个 if 语句 D.一个数组",
        "answer": "A", "difficulty": 3,
        "explanation": "九九乘法表有行有列，外层循环控制行（1~9），内层循环控制列（1~当前行）～两层 for 嵌套最合适，能打印出三角形表格。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "循环嵌套",
        "q_type": "judge",
        "content": "循环嵌套时，内层循环每跑完一轮，外层循环才前进一步。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！外层走一步，内层走完整一圈～就像时钟：分针走一圈，时针才走一格。嵌套循环的总次数通常是各层相乘。",
    },

    # =============== L3 · 综合应用（1 单选 + 1 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面程序输出什么？\\n  int sum = 0;\\n  for (int i = 1; i <= 100; i++) sum += i;\\n  cout << sum;\\nA.5050 B.100 C.505 C.101",
        "answer": "A", "difficulty": 3,
        "explanation": "1+2+…+100 = 5050（高斯小时候算的那个）～sum 一开始 0，每次加 i，循环结束就是 1 到 100 的和。这是循环最经典的例子。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "循环和分支可以组合使用，比如在循环里用 if 判断，根据条件做不同的事。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！循环+分支是编程最常用的组合～比如「循环 1 到 100，遇到偶数就加起来」「遇到 3 的倍数就打印 Fizz」，都靠组合实现。",
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入一个正整数 n，计算 1+2+3+...+n 的和并输出。\\n输入：一个正整数 n（n<=10000）。\\n输出：一个整数，表示 1 到 n 的和。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "用 for 循环：int sum=0; for(int i=1;i<=n;i++) sum+=i; 累加即可～也可以用公式 n*(n+1)/2，但循环练手更重要。注意 sum 要初始化为 0！",
        "grading_rules": _cpp_grading([
            {"input": "100\n", "expected": "5050\n", "hint": "1到100的和"},
            {"input": "1\n", "expected": "1\n", "hint": "只有1"},
            {"input": "10\n", "expected": "55\n", "hint": "1到10的和"},
        ]),
    },
    {
        "syllabus_version": "cpp-l3", "grade_level": 6, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入 n 和 n 个整数，输出其中偶数的个数。\\n输入格式：第一行一个整数 n；第二行 n 个整数，用空格隔开。\\n输出格式：一个整数，表示偶数的个数。",
        "answer": "see_grading_rules", "difficulty": 3,
        "explanation": "用数组存 n 个数，再循环判断每个数：if (a[i] % 2 == 0) count++～count 初始化 0，遇到偶数就加 1。循环+分支+数组三件套！",
        "grading_rules": _cpp_grading([
            {"input": "5\n1 2 3 4 5\n", "expected": "2\n", "hint": "2和4是偶数"},
            {"input": "3\n2 4 6\n", "expected": "3\n", "hint": "全是偶数"},
            {"input": "4\n1 3 5 7\n", "expected": "0\n", "hint": "没有偶数"},
        ]),
    },
]

# =========================================================================
# C++ L4（27 题）：数组与函数基础
# 知识点：二维数组 / 函数定义与调用 / 值传递与作用域 / 递归入门 /
#        简单排序 / 顺序查找
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L4_QUESTIONS = [
    # =============== L4 · 二维数组（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 6, "knowledge_point": "二维数组",
        "q_type": "single",
        "content": "定义一个 3 行 4 列的二维整数数组，正确写法是？A.int a[3][4]; B.int a[3,4]; C.int a(3,4); D.int[3][4] a;",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ 二维数组：类型 名字[行数][列数]～int a[3][4] 是 3 行 4 列。注意是两个方括号分开写，不是逗号。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "二维数组",
        "q_type": "single",
        "content": "int a[3][4]; 这个数组一共有多少个元素？A.12 B.3 C.4 D.7",
        "answer": "A", "difficulty": 3,
        "explanation": "二维数组元素总数 = 行数 × 列数～3 行 × 4 列 = 12 个元素。像 3×4 的格子，一共 12 格。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "二维数组",
        "q_type": "single",
        "content": "遍历一个 m 行 n 列二维数组，一般用什么？A.两层 for 循环嵌套，外层行内层列 B.一层 for 循环 C.一个 if D.一个 while",
        "answer": "A", "difficulty": 3,
        "explanation": "二维有行有列，外层循环行（i=0~m-1），内层循环列（j=0~n-1），a[i][j] 访问每个元素～两层嵌套最自然。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "二维数组",
        "q_type": "judge",
        "content": "二维数组 a[i][j] 中，i 表示行号，j 表示列号。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！a[i][j] 第一个下标 i 是行，第二个 j 是列～和数学里矩阵的 a_ij 一样。行下标、列下标都从 0 开始。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "二维数组",
        "q_type": "judge",
        "content": "二维数组常用来表示矩阵、棋盘、地图等有行列结构的数据。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！矩阵、五子棋棋盘、迷宫地图都是二维的，用二维数组存最合适～a[i][j] 表示第 i 行第 j 列那个位置。",
    },

    # =============== L4 · 函数定义与调用（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "定义一个求两数最大值的函数，正确格式是？A.int max_ab(int a, int b) { return a>b?a:b; } B.function max_ab(a, b) { ... } C.def max_ab(a, b): D.max_ab int(a, b) { }",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ 函数：返回类型 函数名(参数列表) { 函数体 }～int max_ab(int a,int b) 表示返回 int，两个 int 参数。function/def 是其他语言写法。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "函数「返回值类型」是 void 表示什么？A.函数不返回任何值 B.返回整数 C.返回字符 D.返回真或假",
        "answer": "A", "difficulty": 3,
        "explanation": "void 是「空」，表示函数不返回值～这种函数只做事（比如打印），不用 return 返回东西。要返回值就得写具体类型（int/double 等）。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "single",
        "content": "调用函数时给的参数叫「实参」，定义函数时写的参数叫「形参」。下面哪个是实参？A.调用 max_ab(3, 5) 里的 3 和 5 B.定义 int max_ab(int a, int b) 里的 a 和 b C.main 函数 D.return 语句",
        "answer": "A", "difficulty": 3,
        "explanation": "实参是「实际传进去的值」（3、5），形参是「函数定义里占位的变量」（a、b）～调用时实参的值会复制给形参，函数里用形参名操作。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "judge",
        "content": "函数可以把一段重复使用的代码封装起来，需要时调用，避免重复写。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！函数是「代码打包」～写一次求最大值的函数，到处都能调用，不用每次都复制粘贴，改起来也只改一处。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "函数定义与调用",
        "q_type": "judge",
        "content": "函数可以有多个参数，用逗号隔开。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！int add(int a, int b, int c) 三个参数用逗号隔开～参数个数按需要定，调用时也要按顺序传对应个数的实参。",
    },

    # =============== L4 · 值传递与作用域（2 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "值传递与作用域",
        "q_type": "single",
        "content": "C++ 默认的「值传递」有什么特点？A.把实参的值复制一份给形参，函数里改形参不影响外面的实参 B.直接改外面的实参 C.不传值 D.传地址",
        "answer": "A", "difficulty": 3,
        "explanation": "值传递是「复印一份」：实参复制给形参，函数里改的是复印件（形参），原件（实参）不变～想在函数里改外面要用引用传递 &。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "值传递与作用域",
        "q_type": "single",
        "content": "在函数内部定义的变量（局部变量），在函数外面能用吗？A.不能，出了函数就失效 B.能，到处都能用 C.只能在 main 里用 D.只能在特定地方用",
        "answer": "A", "difficulty": 3,
        "explanation": "局部变量只在函数内部有效，函数一结束就「销毁」～这叫「作用域」。函数里定义的 a 和外面的 a 是两回事，互不干扰。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "值传递与作用域",
        "q_type": "judge",
        "content": "局部变量的作用域是从定义它的地方开始，到它所在的代码块（花括号）结束。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！局部变量「生」在定义处，「死」在所在花括号结束处～出了花括号就访问不到了。这避免了不同函数变量名冲突。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "值传递与作用域",
        "q_type": "judge",
        "content": "用值传递时，函数内部修改形参的值，外面的实参会跟着改变。",
        "answer": "false", "difficulty": 3,
        "explanation": "错！值传递是复印，改形参（复印件）不影响实参（原件）～想让函数改外面要用引用传递（参数加 &），那才是「直接改原件」。",
    },

    # =============== L4 · 递归入门（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "递归入门",
        "q_type": "single",
        "content": "「递归」是指什么？A.函数自己调用自己 B.函数调用别的函数 C.函数不调用任何函数 D.循环",
        "answer": "A", "difficulty": 3,
        "explanation": "递归就是「自己调用自己」～比如求阶乘：f(n) = n * f(n-1)，f 函数里又调用 f。递归必须要有「出口」（停止条件），否则无限循环。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "递归入门",
        "q_type": "single",
        "content": "写递归函数最关键的是什么？A.要有递归出口（停止条件），否则会无限递归 B.要用 for 循环 C.要用数组 D.要用全局变量",
        "answer": "A", "difficulty": 3,
        "explanation": "递归必须有「出口」：某个条件不再调用自己，直接返回～比如求阶乘 f(1)=1 就是出口。没有出口会一直调用自己，最后栈溢出崩溃。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "递归入门",
        "q_type": "judge",
        "content": "递归函数必须有递归出口（基准条件），否则会无限递归导致栈溢出。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！没有出口的递归像无限套娃，最终内存爆炸（栈溢出）～出口是「最简单的情况直接返回」，比如 f(1)=1，不再调用自己。",
    },

    # =============== L4 · 简单排序（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "简单排序",
        "q_type": "single",
        "content": "冒泡排序的基本思路是？A.相邻元素两两比较，大的往后冒，一轮下来最大的到最后 B.每次找最小的放最前 C.分治 D.用堆",
        "answer": "A", "difficulty": 3,
        "explanation": "冒泡排序像气泡上浮：相邻两个比，大的往后换，一轮下来最大值「冒」到最后～重复 n-1 轮就排好序。简单但慢。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "简单排序",
        "q_type": "single",
        "content": "选择排序的思路是？A.每次从未排序部分找最小的，放到已排序部分末尾 B.相邻比较交换 C.递归分治 D.用哈希",
        "answer": "A", "difficulty": 3,
        "explanation": "选择排序：每一轮从剩下的数里挑最小的，放到前面～n 轮挑 n 个，排好序。和冒泡比，它交换次数少（每轮最多换一次）。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "简单排序",
        "q_type": "judge",
        "content": "冒泡排序和选择排序的时间复杂度都是 O(n²)。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！这两个简单排序都是 O(n²)～两层循环嵌套，n 大了就慢。后面 L5 会学更快的排序（快排 O(n log n)）。",
    },

    # =============== L4 · 顺序查找（1 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "顺序查找",
        "q_type": "single",
        "content": "顺序查找（线性查找）是怎么找的？A.从头到尾一个一个比对 B.从中间开始找 C.用哈希表 D.排序后找",
        "answer": "A", "difficulty": 2,
        "explanation": "顺序查找就是「挨个看」：从第 0 个看到最后一个，找到就停～最简单直接，但数据多了慢（O(n)）。数据有序可以用更快的二分查找。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "顺序查找",
        "q_type": "judge",
        "content": "顺序查找不要求数组有序，任何数组都能用。",
        "answer": "true", "difficulty": 2,
        "explanation": "对！顺序查找挨个看，不挑数组有没有排过序～但慢（O(n)）。二分查找要求数组有序，但快得多（O(log n)）。",
    },

    # =============== L4 · 综合应用（2 单选 + 1 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面程序输出什么？\\n  int a[5] = {5, 3, 8, 1, 4};\\n  int maxv = a[0];\\n  for (int i = 1; i < 5; i++) if (a[i] > maxv) maxv = a[i];\\n  cout << maxv;\\nA.8 B.5 C.1 D.4",
        "answer": "A", "difficulty": 3,
        "explanation": "这是「找最大值」经典套路：maxv 先存第一个，再循环和后面每个比，更大的就更新～最后 maxv 是 8（5个里最大）。for+if+数组组合。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "写一个求阶乘的递归函数，下面哪个正确？A.int f(int n){ if(n<=1) return 1; return n*f(n-1); } B.int f(int n){ return n*f(n-1); } C.int f(int n){ if(n<=1) return 1; return n*f(n+1); } D.int f(int n){ for(int i=1;i<=n;i++) return i; }",
        "answer": "A", "difficulty": 4,
        "explanation": "阶乘 f(n)=n*f(n-1)，出口 n<=1 返回 1～A 正确。B 没出口会无限递归；C 递归方向反了（n+1）永远到不了出口；D 用了循环不是递归。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "数组和函数可以配合使用：把数组作为参数传给函数，在函数里处理数组元素。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！数组能当函数参数（传数组名）～比如写个 printArray(int a[], int n) 函数打印数组，到处复用。注意数组传参实际传的是地址，函数里改会影响外面。",
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "写一个函数 gcd(int a, int b) 求两个正整数的最大公约数（辗转相除法），并在 main 里读入 a、b 输出结果。\\n输入：一行两个正整数 a b。\\n输出：a 和 b 的最大公约数。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "辗转相除：gcd(a,b) = gcd(b, a%b)，直到 b==0 时 a 就是结果～用 while 循环：while(b!=0){int t=a%b; a=b; b=t;} 最后返回 a。函数封装让代码更清晰。",
        "grading_rules": _cpp_grading([
            {"input": "12 18\n", "expected": "6\n", "hint": "12和18的最大公约数是6"},
            {"input": "7 13\n", "expected": "1\n", "hint": "互质"},
            {"input": "100 60\n", "expected": "20\n", "hint": "100和60的最大公约数"},
        ]),
    },
    {
        "syllabus_version": "cpp-l4", "grade_level": 7, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "从键盘读入 n 和 n 个整数，用冒泡排序将它们从小到大排序后输出。\\n输入：第一行 n；第二行 n 个整数。\\n输出：排序后的 n 个整数，用空格隔开。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "冒泡排序核心：两层循环，外层 n-1 轮，内层每轮比到 n-1-i～相邻比较 a[j]>a[j+1] 就交换。排完依次输出即可。也可用 sort(a, a+n) 但建议手写练手。",
        "grading_rules": _cpp_grading([
            {"input": "5\n3 1 4 1 5\n", "expected": "1 1 3 4 5\n", "hint": "从小到大"},
            {"input": "3\n9 7 8\n", "expected": "7 8 9\n", "hint": "三个数排序"},
            {"input": "1\n5\n", "expected": "5\n", "hint": "单个数"},
        ]),
    },
]

# =========================================================================
# C++ L5（27 题）：字符串与算法进阶
# 知识点：C++ string 类 / 字符数组处理 / 插入与快速排序 / 二分查找 /
#        递归进阶 / 结构体
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L5_QUESTIONS = [
    # =============== L5 · C++ string 类（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 7, "knowledge_point": "C++ string 类",
        "q_type": "single",
        "content": "使用 C++ 的 string 类，需要包含哪个头文件？A.#include <string> B.#include <cstring> C.#include <string.h> D.不用包含",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ 的 string 类在 <string> 里～<cstring> 是 C 风格字符串函数（strlen 等）。用 using namespace std; 后直接写 string s; 即可。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "C++ string 类",
        "q_type": "single",
        "content": "string s = \"hello\"; 求 s 的长度，正确写法是？A.s.length() 或 s.size() B.strlen(s) C.s.len D.length(s)",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ string 用成员函数 s.length() 或 s.size()（带括号，是函数）～strlen 是 C 风格 char 数组用的，string 不能直接用。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "C++ string 类",
        "q_type": "single",
        "content": "string s = \"abc\"; s = s + \"de\"; 后 s 的内容是？A.abcde B.abc C.de D.abc de",
        "answer": "A", "difficulty": 3,
        "explanation": "string 可以用 + 直接拼接～s + \"de\" 把 \"de\" 接到 \"abc\" 后面变 \"abcde\"。比 C 风格的 strcat 方便多了！",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "C++ string 类",
        "q_type": "judge",
        "content": "C++ 的 string 类比 C 风格 char 数组更安全方便，不用手动管理 '\\0' 结束符。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！string 类自动管理内存和长度，不用操心 \\0，还能直接用 +、== 比较～C 风格 char 数组容易越界、要手动管 \\0，string 省心多了。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "C++ string 类",
        "q_type": "judge",
        "content": "可以用 s[i] 访问 string s 的第 i 个字符（下标从 0 开始）。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！string 像数组一样能用下标访问～s[0] 是第一个字符，s[s.length()-1] 是最后一个。和数组下标规则一样从 0 开始。",
    },

    # =============== L5 · 字符数组处理（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "字符数组处理",
        "q_type": "single",
        "content": "把 char 数组 s2 复制到 s1，用哪个函数？A.strcpy(s1, s2) B.strcat(s1, s2) C.strcmp(s1, s2) D.strlen(s1)",
        "answer": "A", "difficulty": 3,
        "explanation": "strcpy(s1, s2) 把 s2 复制到 s1～strcat 是拼接（接到后面），strcmp 是比较，strlen 是求长度。注意 s1 要够大装得下。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "字符数组处理",
        "q_type": "single",
        "content": "strcmp(\"abc\", \"abd\") 的返回值是？A.负数（abc 小于 abd） B.0 C.正数 D.1",
        "answer": "A", "difficulty": 3,
        "explanation": "strcmp 按字典序比较：\"abc\" vs \"abd\"，前两个字符相同，第三个 'c' < 'd'，所以 \"abc\" < \"abd\"，返回负数～相等返回 0，大于返回正数。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "字符数组处理",
        "q_type": "single",
        "content": "判断字符 c 是不是大写字母，正确条件是？A.c >= 'A' && c <= 'Z' B.c >= 'A' || c <= 'Z' C.'A' <= c <= 'Z' D.c isupper",
        "answer": "A", "difficulty": 3,
        "explanation": "大写字母范围 'A'~'Z'，用 && 连两个条件～|| 会几乎对所有字符成立；连续比较 'A'<=c<='Z' 在 C++ 逻辑错；isupper 是函数要写 isupper(c)。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "字符数组处理",
        "q_type": "judge",
        "content": "字符 '0' 的 ASCII 值是 48，'A' 是 65，'a' 是 97。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！记住这几个关键 ASCII：'0'=48，'A'=65，'a'=97～大写字母比小写字母小 32，所以 'A'+32='a'，大小写转换就靠这个差。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "字符数组处理",
        "q_type": "judge",
        "content": "把大写字母 c 转成小写，可以写 c = c + 32; 或 c = c - 'A' + 'a';",
        "answer": "true", "difficulty": 3,
        "explanation": "对！大写比小写小 32，c+32 就变小写～或者 c-'A'+'a' 更易读（先算相对 A 的偏移再加到 a）。也可用 tolower(c) 函数。",
    },

    # =============== L5 · 插入与快速排序（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "插入与快速排序",
        "q_type": "single",
        "content": "插入排序的思路是？A.把每个元素插到前面已排序部分的合适位置 B.相邻交换 C.分治 D.用堆",
        "answer": "A", "difficulty": 3,
        "explanation": "插入排序像整理扑克牌：拿到一张牌，从右往左找合适位置插进去～前面的部分一直是有序的。对近乎有序的数据很快。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "插入与快速排序",
        "q_type": "single",
        "content": "快速排序的平均时间复杂度是？A.O(n log n) B.O(n²) C.O(n) D.O(log n)",
        "answer": "A", "difficulty": 3,
        "explanation": "快排平均 O(n log n)，比冒泡/选择/插入的 O(n²) 快得多～但最坏情况（数据已有序）会退化到 O(n²)。实际中快排很快很常用。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "插入与快速排序",
        "q_type": "judge",
        "content": "快速排序的核心思想是「分治」：选一个基准，比基准小的放左边，大的放右边，再递归排两边。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！快排是经典分治：选基准 → 分成「小、基准、大」三部分 → 左右两边递归快排～分到不能再分就排好了。L7 会更深入学分治。",
    },

    # =============== L5 · 二分查找（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "二分查找",
        "q_type": "single",
        "content": "二分查找要求数组必须满足什么条件？A.数组必须是有序的 B.数组必须无序 C.数组必须是字符数组 D.数组必须是二维的",
        "answer": "A", "difficulty": 3,
        "explanation": "二分查找靠「有序」来砍一半：中间比目标大就砍右半，小就砍左半～无序没法判断砍哪边。所以先排序再用二分查找。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "二分查找",
        "q_type": "single",
        "content": "在 n 个元素的有序数组里二分查找，时间复杂度是？A.O(log n) B.O(n) C.O(n²) D.O(1)",
        "answer": "A", "difficulty": 3,
        "explanation": "每次砍一半，n 个数最多砍 log n 次就剩一个～所以是 O(log n)，比顺序查找 O(n) 快超多。n=100 万只需 20 次！",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "二分查找",
        "q_type": "judge",
        "content": "二分查找每次都取中间元素和目标比较，根据大小关系把查找范围缩小一半。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！mid = (left+right)/2，a[mid] 和目标比：相等找到，目标小就 right=mid-1，目标大就 left=mid+1～范围每次减半，超高效。",
    },

    # =============== L5 · 递归进阶（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "递归进阶",
        "q_type": "single",
        "content": "斐波那契数列：f(1)=1, f(2)=1, f(n)=f(n-1)+f(n-2)。f(5) 等于多少？A.5 B.8 C.3 D.13",
        "answer": "A", "difficulty": 3,
        "explanation": "f(1)=1, f(2)=1, f(3)=f(2)+f(1)=2, f(4)=f(3)+f(2)=3, f(5)=f(4)+f(3)=3+2=5～递归定义，每个数是前两个之和。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "递归进阶",
        "q_type": "single",
        "content": "汉诺塔问题把 n 个盘子从 A 移到 C，需要的最少步数是？A.2^n - 1 B.n C.n² D.2n",
        "answer": "A", "difficulty": 4,
        "explanation": "汉诺塔递推：h(n) = 2*h(n-1) + 1，解出来是 2^n - 1～3 个盘子要 7 步，64 个盘子要 2^64-1 步（传说世界末日才算完）。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "递归进阶",
        "q_type": "judge",
        "content": "递归和循环有时能做同样的事，递归代码通常更简洁但可能更慢、更费内存。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！递归写起来贴近问题本身（更简洁），但每次调用要存现场，比循环费内存、慢一些～像斐波那契递归会有大量重复计算，可用记忆化优化。",
    },

    # =============== L5 · 结构体（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "结构体",
        "q_type": "single",
        "content": "定义一个学生结构体（含姓名和分数），正确写法是？A.struct Student { string name; int score; }; B.struct Student { name, score } C.struct Student(string name, int score) D.Student = struct { ... }",
        "answer": "A", "difficulty": 3,
        "explanation": "C++ 结构体：struct 名字 { 成员列表 };（注意末尾分号）～把多个相关变量打包成一个整体。Student 里有 name 和 score 两个成员。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "结构体",
        "q_type": "single",
        "content": "struct Student { string name; int score; }; 定义 Student s; 后访问 s 的分数，正确写法是？A.s.score B.s->score C.s[score] D.Student.score",
        "answer": "A", "difficulty": 3,
        "explanation": "用点 . 访问结构体成员：s.score～s 是对象用点，s 是指针才用 ->。方括号是数组用的，类型名访问成员没意义。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "结构体",
        "q_type": "judge",
        "content": "结构体数组可以存多个结构体数据，比如 Student stu[100]; 存 100 个学生信息。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！结构体也能开数组～stu[100] 就是 100 个 Student，每个都有 name 和 score。访问 stu[i].score 是第 i 个学生的分数，超方便。",
    },

    # =============== L5 · 综合应用（1 单选 + 2 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面程序对输入 \"abcba\" 输出什么？\\n  string s; cin >> s;\\n  bool ok = true;\\n  for (int i = 0; i < s.length()/2; i++)\\n    if (s[i] != s[s.length()-1-i]) ok = false;\\n  cout << (ok ? \"yes\" : \"no\");\\nA.yes B.no C.abcba D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "这是判断回文串：前后对称位置字符比较～\"abcba\" 第0个'a'==最后'a'，第1个'b'==倒数第2'b'，全相等，ok=true 输出 yes。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "结构体、string、递归、排序等可以组合使用，解决更复杂的问题。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！比如「存学生信息（结构体）→ 按分数排序（快排）→ 二分查找某个分数」～把这些工具组合起来能解决很多实际问题，这就是算法的魅力。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "C++ string 类的 compare 方法或直接用 <、>、== 运算符都可以比较两个字符串的字典序大小。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！string 重载了比较运算符，s1 < s2 直接按字典序比较～也可以用 s1.compare(s2) 返回负/0/正。比 C 风格 strcmp(s1, s2) 更直观，这是 string 类的优势。",
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "读入一个字符串 s（不含空格，长度<=100），判断它是不是回文串（正读反读一样），是输出 yes，不是输出 no。\\n输入：一个字符串 s。\\n输出：yes 或 no。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "回文判断：前后对称位置比，s[i] 和 s[len-1-i]～全部相等就是回文。用 for 循环到 len/2，遇到不等就标记不是。\"abcba\"、\"abba\" 是回文，\"abc\" 不是。",
        "grading_rules": _cpp_grading([
            {"input": "abcba\n", "expected": "yes\n", "hint": "回文"},
            {"input": "abba\n", "expected": "yes\n", "hint": "偶数长度回文"},
            {"input": "abc\n", "expected": "no\n", "hint": "不是回文"},
            {"input": "a\n", "expected": "yes\n", "hint": "单字符是回文"},
        ]),
    },
    {
        "syllabus_version": "cpp-l5", "grade_level": 8, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "用递归求斐波那契数列第 n 项。f(1)=1, f(2)=1, f(n)=f(n-1)+f(n-2)。\\n输入：一个正整数 n（n<=30）。\\n输出：f(n) 的值。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "递归：if(n<=2) return 1; return f(n-1)+f(n-2);～出口 n<=2 返回 1。注意 n 太大（如 50）递归会超时（重复计算多），n<=30 没问题。",
        "grading_rules": _cpp_grading([
            {"input": "5\n", "expected": "5\n", "hint": "f(5)=5"},
            {"input": "1\n", "expected": "1\n", "hint": "f(1)=1"},
            {"input": "10\n", "expected": "55\n", "hint": "f(10)=55"},
        ]),
    },
]

# =========================================================================
# C++ L6（27 题）：数据结构与复杂算法
# 知识点：栈 / 队列 / 单链表 / 贪心算法 / 动态规划入门 / 指针基础
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L6_QUESTIONS = [
    # =============== L6 · 栈（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 8, "knowledge_point": "栈",
        "q_type": "single",
        "content": "栈的特点是？A.后进先出（LIFO） B.先进先出（FIFO） C.随机访问 D.按字母顺序",
        "answer": "A", "difficulty": 3,
        "explanation": "栈像一摞盘子：最后放的最先拿（后进先出 LIFO）～push 压入栈顶，pop 弹出栈顶。队列才是先进先出 FIFO。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "栈",
        "q_type": "single",
        "content": "把 1、2、3 依次入栈，再出栈两次，出栈的元素依次是？A.3、2 B.1、2 C.3、1 D.2、3",
        "answer": "A", "difficulty": 3,
        "explanation": "入栈顺序 1,2,3 后栈里从底到顶是 1,2,3～出栈从顶开始：第一次出 3，第二次出 2。后进先出，3 最后入最先出。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "栈",
        "q_type": "single",
        "content": "下面哪个问题适合用栈解决？A.括号匹配（检查括号是否成对） B.排队买票 C.求最短路径 D.数组求和",
        "answer": "A", "difficulty": 3,
        "explanation": "括号匹配是栈的经典应用：遇到左括号入栈，遇到右括号和栈顶左括号配对出栈～最后栈空说明全配对。排队用队列，最短路径用图算法。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "栈",
        "q_type": "judge",
        "content": "栈只能在栈顶进行插入和删除操作，不能在中间或底部操作。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！栈只开放栈顶一个口～push/pop 都在栈顶，中间和底部的元素碰不到。这是「后进先出」的保证，也是栈和数组的区别。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "栈",
        "q_type": "judge",
        "content": "用数组模拟栈时，需要一个变量 top 记录栈顶位置。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！数组模拟栈：开个数组，top 记录栈顶下标～push 是 a[++top]=x，pop 是 top--。top=-1 表示空栈。这是手写栈的标准做法。",
    },

    # =============== L6 · 队列（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 8, "knowledge_point": "队列",
        "q_type": "single",
        "content": "队列的特点是？A.先进先出（FIFO） B.后进先出（LIFO） C.随机访问 D.二分查找",
        "answer": "A", "difficulty": 3,
        "explanation": "队列像排队买票：先来的先买到（先进先出 FIFO）～从队尾入队，从队头出队。栈才是后进先出。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "队列",
        "q_type": "single",
        "content": "下面哪个适合用队列？A.任务调度（先来先服务） B.撤销操作（最近操作先撤销） C.括号匹配 D.函数调用栈",
        "answer": "A", "difficulty": 3,
        "explanation": "任务调度「先来先做」正是队列～撤销操作/函数调用要「最近先处理」用栈，括号匹配也用栈。队列管「排队」的事。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "队列",
        "q_type": "single",
        "content": "用数组模拟队列，需要哪两个指针？A.队头 front 和队尾 rear B.只有 top C.left 和 right D.head 和 tail（这其实也是队头队尾，但更标准的叫法是 front/rear，本题选 A）",
        "answer": "A", "difficulty": 3,
        "explanation": "队列两端都要动：队头出队 front++，队尾入队 rear++～所以需要 front 和 rear 两个指针。栈只要一个 top，因为只有一端动。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "队列",
        "q_type": "judge",
        "content": "队列的入队操作在队尾，出队操作在队头。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！像排队：新来的人排到队尾（入队），队头的人办完事走人（出队）～两端各管一头，保证先进先出。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "队列",
        "q_type": "judge",
        "content": "广度优先搜索（BFS）通常用队列来实现。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！BFS 一层一层扩展，先访问的先处理，天然契合队列的先进先出～所以 BFS 标配队列，DFS 栈/递归。",
    },

    # =============== L6 · 单链表（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "单链表",
        "q_type": "single",
        "content": "单链表的每个节点包含什么？A.数据 + 指向下一个节点的指针 B.只有数据 C.两个数据 D.数据和数组下标",
        "answer": "A", "difficulty": 3,
        "explanation": "链表节点 = 数据 + next 指针～数据存值，next 指向下一个节点，靠指针把零散节点串起来。和数组不同，链表内存不连续。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "单链表",
        "q_type": "single",
        "content": "和数组相比，链表的最大优点是？A.插入删除快（不用移动大量元素） B.随机访问快 C.内存连续 D.排序快",
        "answer": "A", "difficulty": 3,
        "explanation": "链表插入删除只需改指针，O(1)～数组中间插入要移动后面所有元素 O(n)。但链表不能随机访问（找第 i 个要从头走），这是它的弱项。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "单链表",
        "q_type": "judge",
        "content": "单链表只能从头节点开始，顺着 next 指针往后访问，不能随机访问第 i 个元素。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！链表内存不连续，找第 i 个必须从头走 i 步～不像数组 a[i] 直接定位。所以链表访问 O(n)，数组访问 O(1)，各有所长。",
    },

    # =============== L6 · 贪心算法（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "贪心算法",
        "q_type": "single",
        "content": "贪心算法的核心思想是？A.每一步都选当前看起来最好的，期望得到全局最优 B.把问题分成小问题分别解决 C.试所有可能 D.用递归",
        "answer": "A", "difficulty": 3,
        "explanation": "贪心是「鼠目寸光」：每步选当前最优，不后悔～但贪心不一定得到全局最优（有时会贪小失大），只有满足「贪心选择性质」的问题才适用。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "贪心算法",
        "q_type": "single",
        "content": "找零钱问题（用最少的硬币凑某金额，硬币面额 1、5、10、50、100）用贪心可行吗？A.可以，每次尽量用大面额 B.不行，必须用动态规划 C.用回溯 D.用递归",
        "answer": "A", "difficulty": 3,
        "explanation": "这些面额凑零钱用贪心可行：每次拿能拿的最大面额～比如 63 元：1个50+1个10+3个1=5个。但注意：不是所有面额组合贪心都对（如 1,3,4 凑 6）。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "贪心算法",
        "q_type": "judge",
        "content": "贪心算法不一定能得到全局最优解，只对满足「贪心选择性质」的问题才保证最优。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！贪心是「只看眼前」，有时会错过全局最优～比如某些面额的找零贪心会失败。能用贪心的问题要证明「局部最优能推出全局最优」。",
    },

    # =============== L6 · 动态规划入门（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "动态规划入门",
        "q_type": "single",
        "content": "动态规划的核心两个要素是？A.状态定义和状态转移方程 B.递归和循环 C.数组和指针 D.输入和输出",
        "answer": "A", "difficulty": 4,
        "explanation": "动态规划：定义「状态」（dp[i] 表示什么）+ 写出「状态转移方程」（dp[i] 怎么从前面的 dp 算出来）～这两个搞清楚，DP 就成了一大半。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "动态规划入门",
        "q_type": "single",
        "content": "爬楼梯：每次爬 1 或 2 阶，爬到第 n 阶有几种方法？状态转移是？A.dp[n] = dp[n-1] + dp[n-2] B.dp[n] = dp[n-1] * 2 C.dp[n] = n D.dp[n] = dp[n-1] + 1",
        "answer": "A", "difficulty": 4,
        "explanation": "到第 n 阶只能从 n-1（爬1阶）或 n-2（爬2阶）来～所以方法数 = dp[n-1]+dp[n-2]，和斐波那契一样！这是 DP 最经典的入门题。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "动态规划入门",
        "q_type": "judge",
        "content": "动态规划通过记录子问题的解避免重复计算，通常比纯递归快得多。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！纯递归斐波那契会重复算 f(3) 好多次～DP 把算过的存数组里（记忆化），每个子问题只算一次，时间从 O(2^n) 降到 O(n)。",
    },

    # =============== L6 · 指针基础（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "指针基础",
        "q_type": "single",
        "content": "int a = 5; int *p = &a; 这里 &a 表示什么？A.取变量 a 的地址 B.取 a 的值 C.取指针 D.定义指针",
        "answer": "A", "difficulty": 4,
        "explanation": "& 是「取地址」运算符，&a 得到 a 在内存中的地址～指针 p 存的就是这个地址。* 是解引用（取地址里的值），& 和 * 是反操作。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "指针基础",
        "q_type": "single",
        "content": "int a = 5; int *p = &a; 那么 *p 的值是？A.5 B.a 的地址 C.不确定 D.报错",
        "answer": "A", "difficulty": 4,
        "explanation": "*p 是「解引用」：p 指向 a，*p 就是 a 的值 5～& 取地址，* 取地址里的值，互相配合。p 存地址，*p 拿值。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "指针基础",
        "q_type": "judge",
        "content": "指针变量存的是内存地址，不是具体的值。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！普通变量存值，指针变量存「地址」～就像普通信箱存信，指针存的是「另一信箱的门牌号」。通过门牌号能找到那个信箱（解引用）。",
    },

    # =============== L6 · 综合应用（1 单选 + 1 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "判断一串括号（只有 () ）是否匹配，下面思路哪个对？A.遇左括号入栈，遇右括号弹栈配对，最后栈空则匹配 B.数左右括号数量相等即可 C.用队列 D.用排序",
        "answer": "A", "difficulty": 4,
        "explanation": "数量相等不够（如 )(() 数量相等但不匹配）～栈才是正解：左括号入栈，右括号和栈顶配对出栈，最后栈空且没遇到空栈弹栈才算匹配。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "数据结构（栈、队列、链表）和算法（贪心、DP）是解决复杂问题的基础工具。",
        "answer": "true", "difficulty": 3,
        "explanation": "对！这些都是编程竞赛和实际开发的看家本领～选对数据结构+用对算法，很多看似复杂的问题都能高效解决。L7、L8 会学更高级的。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "指针既可以指向普通变量，也可以指向数组元素，还可以指向链表节点。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！指针很灵活，能指向各种内存～指向变量用 &a，指向数组元素用 &a[i] 或 a+i，指向链表节点用 node 的地址。指针是 C++ 连接各种数据结构的「胶水」。",
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "爬楼梯问题：n 阶楼梯，每次可爬 1 或 2 阶，问有多少种爬法。\\n输入：一个正整数 n（n<=50）。\\n输出：爬到第 n 阶的方法数。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "DP 经典：dp[1]=1, dp[2]=2, dp[i]=dp[i-1]+dp[i-2]～从前往后递推即可。和斐波那契一样，但用循环（不用递归）避免超时，n=50 结果很大用 long long。",
        "grading_rules": _cpp_grading([
            {"input": "1\n", "expected": "1\n", "hint": "1阶1种"},
            {"input": "3\n", "expected": "3\n", "hint": "1+1+1,1+2,2+1"},
            {"input": "5\n", "expected": "8\n", "hint": "f(5)=8"},
        ]),
    },
    {
        "syllabus_version": "cpp-l6", "grade_level": 9, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "括号匹配：读入一个只含 ( 和 ) 的字符串（长度<=1000），判断括号是否完全匹配。是输出 yes，否输出 no。\\n输入：一个字符串 s。\\n输出：yes 或 no。",
        "answer": "see_grading_rules", "difficulty": 4,
        "explanation": "用栈：遇 ( 入栈，遇 ) 若栈空则不匹配，否则弹栈～最后栈空才匹配。注意 ) 多了（栈空还遇 )）和 ( 多了（最后栈非空）两种不匹配情况。",
        "grading_rules": _cpp_grading([
            {"input": "(()())\n", "expected": "yes\n", "hint": "匹配"},
            {"input": "())(\n", "expected": "no\n", "hint": "不匹配"},
            {"input": "((\n", "expected": "no\n", "hint": "左括号多"},
            {"input": ")\n", "expected": "no\n", "hint": "右括号多"},
        ]),
    },
]

# =========================================================================
# C++ L7（27 题）：高级数据结构与算法
# 知识点：STL 容器 / 二叉树遍历 / 动态规划进阶 / 图遍历 DFS&BFS /
#        指针进阶 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L7_QUESTIONS = [
    # =============== L7 · STL 容器（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "STL 容器",
        "q_type": "single",
        "content": "C++ STL 中，vector 是什么？A.动态数组（大小可变） B.固定大小数组 C.链表 D.栈",
        "answer": "A", "difficulty": 4,
        "explanation": "vector 是「动态数组」：能用 push_back 随便加元素，自动扩容～比普通数组灵活（普通数组大小固定）。访问也是 v[i]，O(1)。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "STL 容器",
        "q_type": "single",
        "content": "想存「键值对」（比如学号→姓名），用哪个 STL 容器最合适？A.map B.vector C.set D.stack",
        "answer": "A", "difficulty": 4,
        "explanation": "map 存键值对，按 key 排序～map<int,string> m; m[1]=\"张三\"; 用学号查姓名超方便。set 只存键（不重复集合），vector 是数组，stack 是栈。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "STL 容器",
        "q_type": "single",
        "content": "set 容器的特点是什么？A.元素不重复且自动排序 B.元素可重复 C.元素无序 D.元素固定大小",
        "answer": "A", "difficulty": 4,
        "explanation": "set 是「集合」：元素不重复、自动排序～插入重复元素会被忽略。想可重复用 multiset，想无序快速查找用 unordered_set。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "STL 容器",
        "q_type": "judge",
        "content": "vector 可以用 push_back() 在末尾添加元素，用 size() 获取元素个数。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！vector 最常用的两个操作：v.push_back(x) 末尾加元素，v.size() 返回元素个数～还有 v[i] 访问、v.pop_back() 删末尾，动态管理超方便。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "STL 容器",
        "q_type": "judge",
        "content": "STL 的 sort() 函数默认把元素从小到大排序，需要 #include <algorithm>。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！sort(a, a+n) 把数组 a 的前 n 个元素从小到大排～默认升序，想降序可传 greater<int>()。它在 <algorithm> 里，比手写快排省事。",
    },

    # =============== L7 · 二叉树遍历（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "二叉树遍历",
        "q_type": "single",
        "content": "二叉树的「前序遍历」顺序是？A.根 → 左 → 右 B.左 → 根 → 右 C.左 → 右 → 根 D.右 → 根 → 左",
        "answer": "A", "difficulty": 4,
        "explanation": "前序：根左右（根在「前」）～中序：左根右（根在「中」），后序：左右根（根在「后」）。名字里的「前/中/后」指「根」被访问的位置。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "二叉树遍历",
        "q_type": "single",
        "content": "二叉树的「中序遍历」顺序是？A.左 → 根 → 右 B.根 → 左 → 右 C.左 → 右 → 根 D.根 → 右 → 左",
        "answer": "A", "difficulty": 4,
        "explanation": "中序：左根右（根在「中」间）～对二叉搜索树做中序遍历，结果正好是从小到大排序！这是 BST 的重要性质。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "二叉树遍历",
        "q_type": "single",
        "content": "二叉树通常用什么方式实现遍历最简洁？A.递归 B.循环 C.数组 D.队列",
        "answer": "A", "difficulty": 4,
        "explanation": "二叉树是递归结构（左子树、右子树也是树），用递归遍历最自然～前序：visit(根); dfs(左); dfs(右); 几行搞定。也能用栈非递归实现。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "二叉树遍历",
        "q_type": "judge",
        "content": "二叉树的「后序遍历」顺序是：左子树 → 右子树 → 根节点。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！后序：左右根（根在「后」）～先处理完左右子树，最后访问根。比如删除树要用后序（先删子树再删根），否则删根后子树找不到啦。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "二叉树遍历",
        "q_type": "judge",
        "content": "对二叉搜索树（BST）做中序遍历，得到的序列是有序的（从小到大）。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！BST 性质：左子树所有值 < 根 < 右子树所有值～中序「左根右」正好从小到大访问，所以中序遍历 BST 得到有序序列，这是它的妙用。",
    },

    # =============== L7 · 动态规划进阶（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "动态规划进阶",
        "q_type": "single",
        "content": "最长公共子序列（LCS）问题：序列 X 和 Y 的 LCS。状态 dp[i][j] 表示什么？A.X 前 i 个字符和 Y 前 j 个字符的 LCS 长度 B.X[i] 和 Y[j] 是否相等 C.X 的前 i 个字符和 D.X 和 Y 的长度",
        "answer": "A", "difficulty": 5,
        "explanation": "dp[i][j] = X 前 i 个与 Y 前 j 个的 LCS 长度～转移：若 X[i]==Y[j] 则 dp[i][j]=dp[i-1][j-1]+1，否则 max(dp[i-1][j], dp[i][j-1])。这是二维 DP 经典。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "动态规划进阶",
        "q_type": "single",
        "content": "0-1 背包问题：n 个物品每个有重量和价值，背包容量 W，每个物品最多选一次，求最大价值。状态 dp[i][j] 通常表示？A.前 i 个物品、容量 j 时的最大价值 B.第 i 个物品的价值 C.背包重量 D.物品数量",
        "answer": "A", "difficulty": 5,
        "explanation": "dp[i][j] = 前 i 个物品在容量 j 下的最大价值～转移：不选第 i 个 dp[i-1][j]，选第 i 个 dp[i-1][j-w[i]]+v[i]，取较大。0-1 背包是 DP 招牌题。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "动态规划进阶",
        "q_type": "judge",
        "content": "动态规划常用「滚动数组」优化空间，把二维 dp 压缩成一维，降低内存使用。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！如果 dp[i] 只依赖 dp[i-1]，可以只用一维数组反复覆盖～比如 0-1 背包 dp[j] 从大到小更新，省掉 i 维，空间从 O(nW) 降到 O(W)。",
    },

    # =============== L7 · 图遍历 DFS&BFS（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "图遍历 DFS&BFS",
        "q_type": "single",
        "content": "DFS（深度优先搜索）的特点是？A.一条路走到底再回头 B.一层一层扩展 C.按权值排序 D.随机访问",
        "answer": "A", "difficulty": 4,
        "explanation": "DFS 像「走迷宫不回头」：一条路走到死胡同再退回来换路～用递归或栈实现。BFS 才是一层一层扩展（用队列）。DFS 省内存，BFS 找最短。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "图遍历 DFS&BFS",
        "q_type": "single",
        "content": "BFS（广度优先搜索）用什么数据结构实现？A.队列 B.栈 C.堆 D.数组",
        "answer": "A", "difficulty": 4,
        "explanation": "BFS 一层一层扩展，先访问的先处理，天然契合队列先进先出～所以 BFS 标配队列。DFS 用栈或递归（递归本质也用栈）。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "图遍历 DFS&BFS",
        "q_type": "judge",
        "content": "在无权图中，BFS 可以求出从起点到各点的最短路径（边数最少）。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！无权图 BFS 一层层扩展，第一次到达某点就是最短路径～因为先到的层数少。有权图要用 Dijkstra。这是 BFS 的重要应用。",
    },

    # =============== L7 · 指针进阶（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "指针进阶",
        "q_type": "single",
        "content": "数组名 a 在大多数表达式中表示什么？A.指向数组第一个元素的指针 B.数组的值 C.数组长度 D.数组的最后一个元素",
        "answer": "A", "difficulty": 4,
        "explanation": "数组名 a 是「指向首元素的常量指针」～a 等于 &a[0]。所以 a[i] 等价于 *(a+i)，能用指针算术访问数组。但 a 不能重新赋值（常量）。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "指针进阶",
        "q_type": "single",
        "content": "用指针当函数参数有什么好处？A.可以在函数里修改外面的变量（引用效果）且避免大数组复制 B.运行更快但不修改外面 C.只能读不能写 D.没有好处",
        "answer": "A", "difficulty": 4,
        "explanation": "传指针能在函数里改外面的变量（解引用改值），还能避免大数组整体复制（只传地址）～所以数组传参常传指针。这是指针的核心用途。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "指针进阶",
        "q_type": "judge",
        "content": "指针数组是「存指针的数组」，数组指针是「指向数组的指针」，两者含义不同。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！int *a[10] 是指针数组（10 个指针），int (*a)[10] 是数组指针（指向含 10 元素的数组）～写法差个括号，含义完全不同，要分清。",
    },

    # =============== L7 · 综合应用（3 单选 + 3 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "图的存储用「邻接表」比「邻接矩阵」的优势主要在哪？A.稀疏图（边少）省空间 B.查询两点是否相邻更快 C.稠密图更省 D.遍历更快",
        "answer": "A", "difficulty": 5,
        "explanation": "邻接矩阵 O(V²) 空间，边少时浪费～邻接表 O(V+E)，稀疏图（边少）省空间。但查两点是否相邻，矩阵 O(1) 更快。各有所长。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面哪个数据结构最适合实现「优先队列」（每次取最大或最小元素）？A.堆 B.普通数组 C.链表 D.队列",
        "answer": "A", "difficulty": 5,
        "explanation": "堆是「优先队列」的最佳实现：插入和取最值都 O(log n)～普通数组找最值 O(n)，链表也慢，普通队列不按优先级。堆在 L8 会详细学。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "STL 的 priority_queue 默认是？A.大根堆（每次取最大） B.小根堆（每次取最小） C.队列 D.栈",
        "answer": "A", "difficulty": 4,
        "explanation": "priority_queue 默认大根堆，top() 是最大值～想用小根堆要写 priority_queue<int, vector<int>, greater<int>>。它是堆的封装，O(log n) 操作。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "STL 容器、二叉树、图、动态规划等高级数据结构和算法，是解决复杂问题的强大工具。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！到了 L7，工具箱已经很丰富：vector/map/set 随便用，树和图能处理复杂关系，DP 能解最优子结构问题～组合起来能解大部分竞赛题。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "DFS 常用递归实现，因为图的遍历天然具有递归结构（访问当前节点，再递归访问未访问的邻居）。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！DFS 递归写法超简洁：visit(u); for(每个邻居 v) if(!visited[v]) dfs(v);～用 visited 数组避免重复访问。递归本质用栈，所以也能手写栈非递归。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "动态规划适用于具有「最优子结构」和「重叠子问题」两个性质的问题。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！最优子结构：大问题最优解含小问题最优解；重叠子问题：小问题会被反复计算～DP 用记忆化避免重复算。两个性质都满足才适合 DP。",
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "0-1 背包问题：n 个物品，每个有重量 w[i] 和价值 v[i]，背包容量 W，每个物品选或不选，求能装的最大总价值。\\n输入：第一行 n 和 W；接下来 n 行每行 w[i] v[i]。\\n输出：最大总价值。\\n约束：n<=100, W<=1000。",
        "answer": "see_grading_rules", "difficulty": 5,
        "explanation": "DP：dp[j] 表示容量 j 的最大价值，对每个物品从大到小更新 dp[j]=max(dp[j], dp[j-w[i]]+v[i])～滚动数组优化空间到 O(W)。注意 0-1 背包要倒序更新避免重复选。",
        "grading_rules": _cpp_grading([
            {"input": "4 5\n2 3\n1 2\n3 4\n2 2\n", "expected": "7\n", "hint": "选物品1,2,4：2+1+2=5<=5，价值3+2+2=7"},
            {"input": "3 10\n5 10\n4 7\n6 8\n", "expected": "17\n", "hint": "选物品1和3"},
            {"input": "1 3\n5 100\n", "expected": "0\n", "hint": "装不下"},
        ]),
    },
    {
        "syllabus_version": "cpp-l7", "grade_level": 10, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "最长公共子序列（LCS）：给定两个字符串 s1 和 s2（长度<=1000），求它们的最长公共子序列长度。\\n输入：两行，每行一个字符串。\\n输出：LCS 的长度。",
        "answer": "see_grading_rules", "difficulty": 5,
        "explanation": "二维 DP：dp[i][j] 表示 s1 前 i 个和 s2 前 j 个的 LCS 长度～若 s1[i-1]==s2[j-1] 则 dp[i][j]=dp[i-1][j-1]+1，否则 max(dp[i-1][j], dp[i][j-1])。答案在 dp[n][m]。",
        "grading_rules": _cpp_grading([
            {"input": "ABCBDAB\nBDCAB\n", "expected": "4\n", "hint": "LCS=BCAB长度4"},
            {"input": "abc\nabc\n", "expected": "3\n", "hint": "完全相同"},
            {"input": "abc\ndef\n", "expected": "0\n", "hint": "无公共"},
        ]),
    },
]

# =========================================================================
# C++ L8（27 题）：综合算法与工程化基础
# 知识点：面向对象基础 / 图论算法 / 复杂动态规划 / 二叉搜索树与堆 /
#        代码优化与工程化 / 综合应用
# 题型分布：15 单选 + 10 判断 + 2 编程
# =========================================================================
CPP_L8_QUESTIONS = [
    # =============== L8 · 面向对象基础（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "面向对象基础",
        "q_type": "single",
        "content": "C++ 中定义「类」用哪个关键字？A.class B.struct C.type D.object",
        "answer": "A", "difficulty": 4,
        "explanation": "class 定义类～class Student { ... }; 把数据和函数打包成一个整体。struct 也能定义类（默认权限不同），但习惯上 class 表示有行为的类型。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "面向对象基础",
        "q_type": "single",
        "content": "类的「构造函数」有什么特点？A.名字和类名相同，没有返回类型，对象创建时自动调用 B.返回 int C.有返回类型 D.手动调用",
        "answer": "A", "difficulty": 4,
        "explanation": "构造函数名字 = 类名，无返回类型，对象诞生时自动调用～用来初始化对象。比如 Student(string n){name=n;} 创建时就设好名字。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "面向对象基础",
        "q_type": "single",
        "content": "public 和 private 的区别是？A.public 成员外部能访问，private 只能类内部访问 B.public 是公有的，private 是私有的，没区别 C.private 外部能访问 D.public 不能访问",
        "answer": "A", "difficulty": 4,
        "explanation": "public（公有）外部能访问，private（私有）只有类自己的成员函数能访问～这是「封装」：把数据藏起来（private），只暴露接口（public）。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "面向对象基础",
        "q_type": "judge",
        "content": "面向对象的三大特性是：封装、继承、多态。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！封装（藏数据露接口）、继承（子类复用父类）、多态（同一接口不同实现）是 OOP 三大支柱～L8 主要学封装，继承和多态更深入但也是基础。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "面向对象基础",
        "q_type": "judge",
        "content": "类的私有成员（private）只能在类的成员函数内部访问，外部不能直接访问。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！private 是「保险箱」，只有类自己的函数能开～外部要访问得通过 public 的成员函数（getter/setter）。这保护数据不被乱改。",
    },

    # =============== L8 · 图论算法（3 单选 + 2 判断） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "图论算法",
        "q_type": "single",
        "content": "Dijkstra 算法用于解决什么问题？A.单源最短路径（非负权图） B.最小生成树 C.网络流 D.拓扑排序",
        "answer": "A", "difficulty": 5,
        "explanation": "Dijkstra 求单源最短路径：从一个点到其他所有点的最短路～要求边权非负（负权用 Bellman-Ford）。用堆优化 O((V+E)log V)。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "图论算法",
        "q_type": "single",
        "content": "求「最小生成树」的常用算法有？A.Prim 和 Kruskal B.Dijkstra 和 Floyd C.DFS 和 BFS D.快排和归并",
        "answer": "A", "difficulty": 5,
        "explanation": "最小生成树：Prim（从点扩展，适合稠密图）和 Kruskal（按边权排序+并查集，适合稀疏图）～Dijkstra 是最短路径，DFS/BFS 是遍历。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "图论算法",
        "q_type": "single",
        "content": "Floyd 算法求什么？A.所有点对之间的最短路径 B.单源最短路径 C.最小生成树 D.拓扑排序",
        "answer": "A", "difficulty": 5,
        "explanation": "Floyd 求所有点对最短路：三重循环 dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])～O(V³)，代码超短但慢，适合 V 小或稠密图。能处理负权（无负环）。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "图论算法",
        "q_type": "judge",
        "content": "Dijkstra 算法不能处理有负权边的图，有负权要用 Bellman-Ford 或 SPFA。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！Dijkstra 基于「已确定的最短路不会变」的贪心，负权会破坏这个假设～有负权用 Bellman-Ford（能检测负环）或 SPFA。这是重要限制。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "图论算法",
        "q_type": "judge",
        "content": "Kruskal 算法求最小生成树时，需要用「并查集」来判断加入的边是否形成环。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！Kruskal 按边权从小到大加边，加之前用并查集查两端点是否已连通～连通则加这条边会成环，跳过；不连通才加。并查集是 Kruskal 的关键。",
    },

    # =============== L8 · 复杂动态规划（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "复杂动态规划",
        "q_type": "single",
        "content": "「多重背包」和「0-1 背包」的区别是？A.多重背包每个物品有多个（限量），0-1 背包每个只有 1 个 B.多重背包物品无限 C.完全一样 D.多重背包没有重量",
        "answer": "A", "difficulty": 5,
        "explanation": "0-1 背包每物品 1 个（选或不选）；多重背包每物品有 c[i] 个（选 0~c[i] 个）；完全背包每物品无限个～多重背包可用二进制拆分或单调队列优化。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "复杂动态规划",
        "q_type": "single",
        "content": "「区间 DP」的特点是？A.状态是「区间 [i,j]」，从小区间合并成大区间 B.状态是一维的 C.只能用递归 D.没有状态转移",
        "answer": "A", "difficulty": 5,
        "explanation": "区间 DP：dp[i][j] 表示区间 [i,j] 上的最优值，通过枚举断点 k 把 [i,j] 拆成 [i,k]+[k+1,j] 合并～经典题如石子合并、矩阵链乘。先算小区间再合并。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "复杂动态规划",
        "q_type": "judge",
        "content": "动态规划可以按状态维度分类：一维 DP、二维 DP、区间 DP、树形 DP、状压 DP 等。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！DP 家族庞大：一维（爬楼梯）、二维（LCS）、区间（石子合并）、树形（树的最大独立集）、状压（旅行商）～按问题结构选合适的 DP 形态。",
    },

    # =============== L8 · 二叉搜索树与堆（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "二叉搜索树与堆",
        "q_type": "single",
        "content": "二叉搜索树（BST）的性质是？A.左子树所有值 < 根 < 右子树所有值 B.左 > 根 > 右 C.完全二叉树 D.每层满",
        "answer": "A", "difficulty": 5,
        "explanation": "BST：左子树值 < 根 < 右子树值（且左右子树也是 BST）～这让查找/插入/删除都 O(log n)（平衡时）。中序遍历 BST 得到有序序列。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "二叉搜索树与堆",
        "q_type": "single",
        "content": "「堆」的性质是？A.父节点 >=（或 <=）子节点，是完全二叉树 B.左 < 父 < 右 C.任意结构 D.叶子节点都在最左",
        "answer": "A", "difficulty": 5,
        "explanation": "堆是完全二叉树 + 父子大小关系：大根堆父>=子（根最大），小根堆父<=子（根最小）～只保证「堆序性」不像 BST 那样左右有序。priority_queue 就是堆。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 11, "knowledge_point": "二叉搜索树与堆",
        "q_type": "judge",
        "content": "堆的插入和删除（取堆顶）操作时间复杂度都是 O(log n)。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！堆是完全二叉树，高度 O(log n)～插入「上浮」、取堆顶「下沉」都最多走树高，所以 O(log n)。这让堆成为实现优先队列的高效结构。",
    },

    # =============== L8 · 代码优化与工程化（2 单选 + 1 判断） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "代码优化与工程化",
        "q_type": "single",
        "content": "C++ 异常处理用哪组关键字？A.try-catch-throw B.if-else C.for-while D.begin-end",
        "answer": "A", "difficulty": 4,
        "explanation": "try 包住可能出错的代码，throw 抛出异常，catch 捕获处理～比让程序崩溃友好。但异常有性能开销，性能敏感场景（如竞赛）慎用。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "代码优化与工程化",
        "q_type": "single",
        "content": "多文件编程中，函数声明通常放在哪里？A..h 头文件 B..cpp 源文件 C.README D.注释里",
        "answer": "A", "difficulty": 4,
        "explanation": "声明放 .h（头文件），实现放 .cpp～别的文件 #include 头文件就能用这些函数。这是模块化：把代码分到多个文件，便于管理和复用。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "代码优化与工程化",
        "q_type": "judge",
        "content": "在算法竞赛中，常见的优化技巧包括：读入优化（快速 IO）、减少常数、空间换时间（预处理）、选择合适算法等。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！快速 IO（scanf/printf 或自定义读入）能省大量时间～减少常数（少用 STL 低效操作）、预处理查表、选对算法（O(n log n) 替 O(n²)）都是常用手段。",
    },

    # =============== L8 · 综合应用（3 单选 + 3 判断 + 2 编程） ===============
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "下面哪个排序算法的最坏时间复杂度是 O(n²)？A.快速排序 B.归并排序 C.堆排序 D.计数排序",
        "answer": "A", "difficulty": 5,
        "explanation": "快排最坏 O(n²)（数据已有序且基准选得差）～归并和堆最坏都是 O(n log n) 稳定，计数排序 O(n+k)。所以快排虽快但有最坏情况，可随机化基准规避。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "「分治」算法的三个步骤是？A.分解 → 解决 → 合并 B.输入 → 处理 → 输出 C.定义 → 调用 → 返回 D.排序 → 查找 → 输出",
        "answer": "A", "difficulty": 5,
        "explanation": "分治三步：分解（大问题拆小）→ 解决（递归解小问题）→ 合并（把小问题解合成大问题解）～归并排序、快排都是分治经典。分治是高级算法的核心思想。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "single",
        "content": "并查集主要用于解决什么问题？A.动态连通性问题（判断元素是否属于同一集合、合并集合） B.最短路径 C.排序 D.字符串匹配",
        "answer": "A", "difficulty": 5,
        "explanation": "并查集：find 查根、union 合并集合，近 O(1)～判断连通、Kruskal 检测环、集合合并都靠它。带路径压缩和按秩合并的并查集是神器。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "面向对象、图论、动态规划、高级数据结构等综合运用，能解决大部分复杂算法问题。",
        "answer": "true", "difficulty": 4,
        "explanation": "对！L8 是 C++ 考纲的高峰：OOP 让代码工程化，图论/DP/高级数据结构解决复杂问题～这些是信息学竞赛和实际开发的核心能力，组合使用威力巨大。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "归并排序是「分治」思想的典型应用，且是稳定排序。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！归并排序：拆两半（分）→ 递归排两半（治）→ 合并两个有序序列（合）～时间 O(n log n) 稳定，需要 O(n) 额外空间。是分治+稳定的代表。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "judge",
        "content": "时间复杂度 O(n log n) 的排序算法有：归并排序、堆排序、快速排序（平均）。",
        "answer": "true", "difficulty": 5,
        "explanation": "对！这三个都 O(n log n)：归并稳定最坏也是，堆最坏也是，快排平均是（最坏 O(n²)）～它们比 O(n²) 的冒泡/选择/插入快得多，是高级排序。",
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "完全背包问题：n 种物品，第 i 种有重量 w[i] 和价值 v[i]，每种物品有无限个，背包容量 W，求最大总价值。\\n输入：第一行 n 和 W；接下来 n 行每行 w[i] v[i]。\\n输出：最大总价值。\\n约束：n<=100, W<=1000。",
        "answer": "see_grading_rules", "difficulty": 5,
        "explanation": "完全背包：dp[j] 表示容量 j 的最大价值，对每个物品从小到大更新 dp[j]=max(dp[j], dp[j-w[i]]+v[i])～注意和 0-1 背包相反要正序更新（允许重复选）。",
        "grading_rules": _cpp_grading([
            {"input": "3 7\n3 4\n4 5\n2 3\n", "expected": "10\n", "hint": "选2个物品3和1个物品1或类似最优"},
            {"input": "2 10\n1 1\n2 1\n", "expected": "10\n", "hint": "全选物品1（价值密度最高）"},
            {"input": "1 5\n3 10\n", "expected": "10\n", "hint": "选1个，剩2容量不够再选"},
        ]),
    },
    {
        "syllabus_version": "cpp-l8", "grade_level": 12, "knowledge_point": "综合应用",
        "q_type": "program", "program_lang": "cpp",
        "content": "定义一个类 Rectangle，有长和宽（私有），有构造函数、计算面积的成员函数 area()。在 main 中读入长和宽，创建对象，输出面积。\\n输入：一行两个整数 length width。\\n输出：矩形面积（length * width）。",
        "answer": "see_grading_rules", "difficulty": 5,
        "explanation": "面向对象练手：class Rectangle { private: int l, w; public: Rectangle(int a,int b):l(a),w(b){} int area(){return l*w;} };～main 里 Rectangle r(l,w); cout<<r.area();。封装数据+行为。",
        "grading_rules": _cpp_grading([
            {"input": "3 4\n", "expected": "12\n", "hint": "3*4=12"},
            {"input": "5 5\n", "expected": "25\n", "hint": "5*5=25"},
            {"input": "1 10\n", "expected": "10\n", "hint": "1*10=10"},
        ]),
    },
]


# =========================================================================
# 汇总：所有 C++ 题目（8 级 × 27 题 = 216 题）
# =========================================================================
ALL_CPP_QUESTIONS = (
    CPP_L1_QUESTIONS
    + CPP_L2_QUESTIONS
    + CPP_L3_QUESTIONS
    + CPP_L4_QUESTIONS
    + CPP_L5_QUESTIONS
    + CPP_L6_QUESTIONS
    + CPP_L7_QUESTIONS
    + CPP_L8_QUESTIONS
)


# =========================================================================
# 各级题目列表映射（方便按级别取用）
# =========================================================================
CPP_QUESTIONS_BY_LEVEL = {
    "cpp-l1": CPP_L1_QUESTIONS,
    "cpp-l2": CPP_L2_QUESTIONS,
    "cpp-l3": CPP_L3_QUESTIONS,
    "cpp-l4": CPP_L4_QUESTIONS,
    "cpp-l5": CPP_L5_QUESTIONS,
    "cpp-l6": CPP_L6_QUESTIONS,
    "cpp-l7": CPP_L7_QUESTIONS,
    "cpp-l8": CPP_L8_QUESTIONS,
}


def _verify():
    """自检：题目总数、各级数量、题型分布。"""
    total = len(ALL_CPP_QUESTIONS)
    print(f"总题数: {total}（应为 216）")
    assert total == 216, f"题目总数不对: {total} != 216"

    from collections import Counter

    by_level = Counter(q["syllabus_version"] for q in ALL_CPP_QUESTIONS)
    print("\n各级题数:")
    for lv in range(1, 9):
        key = f"cpp-l{lv}"
        cnt = by_level[key]
        print(f"  {key}: {cnt} 题（应为 27）")
        assert cnt == 27, f"{key} 题数不对: {cnt} != 27"

    print("\n各级题型分布:")
    for lv in range(1, 9):
        key = f"cpp-l{lv}"
        qs = CPP_QUESTIONS_BY_LEVEL[key]
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
    for q in ALL_CPP_QUESTIONS:
        need = required_fields[q["q_type"]]
        missing = need - set(q.keys())
        assert not missing, f"题目缺字段 {missing}: {q['content'][:30]}..."
        # program 题必须有 program_lang=cpp
        if q["q_type"] == "program":
            assert q["program_lang"] == "cpp", f"编程题 program_lang 不是 cpp: {q['content'][:30]}"
    print("  全部题目字段完整 ✓")

    # 各级知识点覆盖
    print("\n各级知识点:")
    for lv in range(1, 9):
        key = f"cpp-l{lv}"
        kps = []
        for q in CPP_QUESTIONS_BY_LEVEL[key]:
            if q["knowledge_point"] not in kps:
                kps.append(q["knowledge_point"])
        print(f"  {key}: {' / '.join(kps)}")

    print("\n[verify] 全部检查通过 ✓")


if __name__ == "__main__":
    _verify()
