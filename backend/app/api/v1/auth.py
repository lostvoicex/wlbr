"""认证路由：/api/v1/auth/*

说明：
- 学员手机号+验证码：为了不引入短信平台依赖，这里做占位实现——
  接受任意 4-6 位数字验证码。真实上线前替换成"发码/校验"流程。
- 学员学号+密码：需要 students 表中存在该 id 且已设置 password_hash。
- 老师登录：从数据库 teachers 表查询，若表为空则自动创建默认演示账号。
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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

router = APIRouter(prefix="/auth", tags=["auth"])


# 默认演示老师账号（teachers 表为空时自动创建）
_DEFAULT_TEACHERS: list[dict[str, str]] = [
    {"teacher_no": "T001", "password": "teacher123", "name": "王老师", "role": "teacher"},
    {"teacher_no": "T002", "password": "teacher123", "name": "李老师", "role": "teacher"},
    {"teacher_no": "admin", "password": "admin123", "name": "管理员", "role": "admin"},
]


def _ensure_default_teachers(db: Session) -> None:
    """如果 teachers 表为空，自动创建默认演示账号。"""
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
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    if payload.mode == "student_phone":
        # 占位：任意 4-6 位数字验证码通过，且需要 phone 已注册
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
        return _issue_token_pair(subject=str(student.id), role="student")

    if payload.mode == "teacher":
        # 首次登录时确保有默认演示账号
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
        return _issue_token_pair(subject=teacher.teacher_no, role=teacher.role)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未知登录方式")


@router.post("/refresh", response_model=TokenPair, summary="刷新 access token")
def refresh_token(payload: RefreshRequest) -> TokenPair:
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
    return _issue_token_pair(subject=sub, role=role)
