"""认证相关 schemas。"""
from typing import Literal

from pydantic import BaseModel, Field

LoginMode = Literal["student_phone", "student_id", "teacher"]


class LoginRequest(BaseModel):
    """登录请求：
    - student_phone：学员用手机号 + 验证码登录（M1 骨架里验证码任意 4-6 位均通过，占位实现）
    - student_id：学员用学号（对应 students.id 或后续 student_no 字段）+ 密码登录
    - teacher：老师用工号/手机号 + 密码登录
    """

    mode: LoginMode = Field(..., description="登录方式")
    account: str = Field(..., min_length=1, max_length=64, description="账号")
    credential: str = Field(..., min_length=1, max_length=128, description="密码或验证码")


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    subject: str


class RefreshRequest(BaseModel):
    refresh_token: str
