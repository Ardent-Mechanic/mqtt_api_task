from pathlib import Path
from typing import Optional

from pydantic import SecretStr, BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    metric: str = "/metric"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: str
    # password: SecretStr = 'root'
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    @field_validator('url')
    def validate_url(cls, v):
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("URL должен начинаться с 'postgresql+asyncpg://'")
        return v


class MQTTConfig(BaseModel):
    host: str = "dev.rvts.ru"
    port: int = 1883
    topic: str = "sensor/802241/data"
    username: Optional[str] = None
    password: Optional[SecretStr] = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    mqtt_config: MQTTConfig = MQTTConfig()
    db: DatabaseConfig


settings = Settings()
