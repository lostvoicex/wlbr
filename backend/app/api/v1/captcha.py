"""图形验证码路由：/api/v1/captcha/*

生成简单的算术验证码或图片验证码，用于登录页防机器人。
验证码存储在内存中，有过期时间。
"""
import io
import random
import string
import time
import uuid
from typing import Dict, Tuple

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/captcha", tags=["captcha"])

# 内存存储：captcha_id -> (answer, expire_timestamp)
_store: Dict[str, Tuple[str, float]] = {}
_CAPTCHA_TTL = 300  # 5 分钟过期


def _gc() -> None:
    now = time.time()
    expired = [k for k, (_, exp) in _store.items() if exp < now]
    for k in expired:
        del _store[k]


def _generate_text(length: int = 4) -> str:
    chars = string.ascii_uppercase + string.digits
    # 去除容易混淆的字符
    chars = chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "").replace("l", "")
    return "".join(random.choice(chars) for _ in range(length))


def _render_image(text: str) -> bytes:
    """用 Pillow 生成验证码图片。"""
    from PIL import Image, ImageDraw, ImageFont

    width, height = 120, 40
    img = Image.new("RGB", (width, height), color=(255, 250, 245))
    draw = ImageDraw.Draw(img)

    # 噪点
    for _ in range(60):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        draw.point((x, y), fill=(random.randint(150, 230), random.randint(150, 230), random.randint(150, 230)))

    # 干扰线
    for _ in range(3):
        x1 = random.randint(0, width // 3)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(width // 2, width - 1)
        y2 = random.randint(0, height - 1)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=1)

    # 文字
    font = None
    for font_name in ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]:
        try:
            font = ImageFont.truetype(font_name, 28)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    x_offset = 10
    for ch in text:
        color = (random.randint(20, 120), random.randint(20, 120), random.randint(80, 180))
        y_offset = random.randint(-2, 4)
        draw.text((x_offset, y_offset), ch, fill=color, font=font)
        x_offset += 26

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class CaptchaResponse(BaseModel):
    captcha_id: str
    expires_in: int = _CAPTCHA_TTL


@router.get("/image", response_class=StreamingResponse, summary="获取图形验证码图片")
def get_captcha_image() -> StreamingResponse:
    _gc()
    text = _generate_text()
    captcha_id = str(uuid.uuid4())
    _store[captcha_id] = (text.upper(), time.time() + _CAPTCHA_TTL)
    image_bytes = _render_image(text)
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")


@router.get("/new", response_model=CaptchaResponse, summary="创建验证码并返回 ID（前端用 ID 拼图片 URL）")
def create_captcha() -> CaptchaResponse:
    _gc()
    captcha_id = str(uuid.uuid4())
    # 预生成答案
    text = _generate_text()
    _store[captcha_id] = (text.upper(), time.time() + _CAPTCHA_TTL)
    return CaptchaResponse(captcha_id=captcha_id)


def verify_captcha(captcha_id: str, captcha_code: str) -> bool:
    """校验验证码，成功后自动销毁（一次性）。"""
    _gc()
    if not captcha_id or not captcha_code:
        return False
    entry = _store.get(captcha_id)
    if not entry:
        return False
    answer, expire = entry
    if time.time() > expire:
        del _store[captcha_id]
        return False
    if answer.upper() != captcha_code.strip().upper():
        del _store[captcha_id]
        return False
    # 验证成功，销毁
    del _store[captcha_id]
    return True
