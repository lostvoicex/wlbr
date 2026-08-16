"""认证路由：/api/v1/auth/*

说明：
- 学员手机号+验证码：需配合图形验证码使用，手机号需已注册
- 学员学号+密码：需要 students 表中存在该 id 且已设置 password_hash
- 老师登录：从数据库 teachers 表查询，开发环境自动创建演示账号
- 登录速率限制：同一账号+IP 每分钟最多 5 次尝试
"""
import time
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import (
    JWTError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db import get_db
from app.models import Student, Teacher
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.api.v1.captcha import verify_captcha

router = APIRouter(prefix="/auth", tags=["auth"])

# 简单内存速率限制：key -> [(timestamp, ...)]
_rate_store: Dict[str, List[float]] = {}
_RATE_WINDOW = 60  # 60 秒窗口
_RATE_MAX = 5  # 每窗口最多 5 次


def _check_rate_limit(key: str) -> None:
    now = time.time()
    attempts = _rate_store.get(key, [])
    recent = [t for t in attempts if now - t < _RATE_WINDOW]
    if len(recent) >= _RATE_MAX:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="尝试太多次了，请等一分钟再试～",
        )
    recent.append(now)
    _rate_store[key] = recent


def _clear_rate_limit(key: str) -> None:
    _rate_store.pop(key, None)


# 默认演示老师账号（仅开发环境，teachers 表为空时自动创建）
_DEFAULT_TEACHERS: list[dict[str, str]] = [
    {"teacher_no": "T001", "password": "teacher123", "name": "王老师", "role": "teacher"},
    {"teacher_no": "T002", "password": "teacher123", "name": "李老师", "role": "teacher"},
    {"teacher_no": "admin", "password": "admin123", "name": "管理员", "role": "admin"},
]


def _ensure_default_teachers(db: Session) -> None:
    """开发环境：teachers 表为空时自动创建演示账号。生产环境跳过。"""
    if settings.is_prod:
        return
    count = db.query(Teacher).count()
    if count > 0:
        return
    for item in _DEFAULT_TEACHERS:
        teacher = Teacher(
            teacher_no=item["teacher_no"],
            name=item["name"],
            role=item["role"],
            password_hash=hash_password(item["password"]),
            status="active",
        )
        db.add(teacher)
    db.commit()


def _issue_token_pair(subject: str, role: str) -> TokenPair:
    return TokenPair(
        access_token=create_access_token(subject, role),
        refresh_token=create_refresh_token(subject, role),
        role=role,
        subject=subject,
    )


@router.post("/login", response_model=TokenPair, summary="统一登录入口")
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenPair:
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"{payload.account}:{client_ip}"
    _check_rate_limit(rate_key)

    # 校验图形验证码
    if not verify_captcha(payload.captcha_id, payload.captcha_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码不对，看不清楚可以换一张哦",
        )

    if payload.mode == "student_phone":
        code = payload.credential.strip()
        if not (code.isdigit() and 4 <= len(code) <= 6):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码格式不对，应该是 4-6 位数字",
            )
        student = db.query(Student).filter(Student.phone == payload.account).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="没有找到这个手机号对应的小朋友，请先联系老师注册",
            )
        _clear_rate_limit(rate_key)
        return _issue_token_pair(subject=str(student.id), role="student")

    if payload.mode == "student_id":
        try:
            sid = int(payload.account)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="学号必须是数字哦"
            )
        student = db.query(Student).filter(Student.id == sid).first()
        if not student or not student.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="学号或密码不对，再试一次！"
            )
        if not verify_password(payload.credential, student.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="学号或密码不对，再试一次！"
            )
        _clear_rate_limit(rate_key)
        return _issue_token_pair(subject=str(student.id), role="student")

    if payload.mode == "teacher":
        _ensure_default_teachers(db)

        acct = payload.account.strip()
        teacher = (
            db.query(Teacher)
            .filter(Teacher.teacher_no == acct, Teacher.status == "active")
            .first()
        )
        if not teacher or not verify_password(payload.credential, teacher.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="工号或密码错误",
            )
        _clear_rate_limit(rate_key)
        return _issue_token_pair(subject=teacher.teacher_no, role=teacher.role)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未知登录方式")


@router.post("/refresh", response_model=TokenPair, summary="刷新 access token")
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    try:
        decoded = decode_token(payload.refresh_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token 无效或已过期"
        )
    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="传入的不是 refresh token"
        )
    sub = decoded.get("sub")
    role = decoded.get("role")
    if not sub or not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="refresh token 载荷不完整"
        )

    if role == "student":
        try:
            sid = int(sub)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户信息异常，请重新登录"
            )
        if not db.query(Student).filter(Student.id == sid).first():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="账号不存在，请重新登录"
            )
    elif role in ("teacher", "admin"):
        teacher = (
            db.query(Teacher)
            .filter(Teacher.teacher_no == sub, Teacher.status == "active")
            .first()
        )
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="账号已停用或不存在，请联系管理员"
            )

    return _issue_token_pair(subject=sub, role=role)
