"""题库数据包：按语言 + 级别分文件存放原始题目数据。

文件清单：
- scratch_questions_data.py  : Scratch L1-L4（4 级 × 27 题 = 108 题）
- cpp_questions_data.py      : C++ L1-L8（8 级 × 27 题 = 216 题）
- python_questions_data.py   : Python L1-L6（6 级 × 27 题 = 162 题）

合计 18 级 × 27 题 = 486 题，统一由 app.seed 汇总导入。
"""
from app.data.scratch_questions_data import ALL_SCRATCH_QUESTIONS
from app.data.cpp_questions_data import ALL_CPP_QUESTIONS
from app.data.python_questions_data import ALL_PYTHON_QUESTIONS

# 汇总：18 级 × 27 题 = 486 题
ALL_QUESTIONS = (
    ALL_SCRATCH_QUESTIONS
    + ALL_CPP_QUESTIONS
    + ALL_PYTHON_QUESTIONS
)

__all__ = [
    "ALL_SCRATCH_QUESTIONS",
    "ALL_CPP_QUESTIONS",
    "ALL_PYTHON_QUESTIONS",
    "ALL_QUESTIONS",
]
