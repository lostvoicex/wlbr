"""认证相关 schemas。"""
from typing import Literal, Optional

from pydantic import BaseModel, Field

LoginMode = Literal["student_phone", "student_id", "teacher"]


class LoginRequest(BaseModel):
    """登录请求：
    - student_phone：学员用手机号 + 验证码登录
    - student_id：学员用学号 + 密码登录
    - teacher：老师用工号 + 密码登录
    """

    mode: LoginMode = Field(..., description="登录方式")
    account: str = Field(..., min_length=1, max_length=64, description="账号")
    credential: str = Field(..., min_length=1, max_length=128, description="密码或验证码")
    captcha_id: str = Field(..., description="验证码 ID")
    captcha_code: str = Field(..., min_length=1, max_length=10, description="图形验证码")


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    subject: str


class RefreshRequest(BaseModel):
    refresh_token: str
