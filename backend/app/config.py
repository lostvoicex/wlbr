"""全局配置：读取环境变量。"""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量 / .env 加载配置。"""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 应用元信息
    app_name: str = "瓦力贝尔编程薄弱定位平台"
    app_env: str = Field(default="dev")
    api_prefix: str = "/api/v1"

    # 数据库
    database_url: str = Field(
        default="sqlite:///./wali_bell.db",
        description="SQLAlchemy 数据库连接串，生产使用 postgresql+psycopg://...",
    )

    # JWT
    jwt_secret_key: str = Field(default="change-me-in-prod")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=60)
    jwt_refresh_token_expire_days: int = Field(default=14)

    # CORS
    cors_allow_origins: str = Field(
        default="http://localhost:5000,http://127.0.0.1:5000"
    )

    # 服务端口
    backend_port: int = Field(default=8000)

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
