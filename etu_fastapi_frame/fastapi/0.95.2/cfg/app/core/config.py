# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 17:10
# @Author  : Jieay
# @File    : config.py
import os
# import base64
# import secrets
from urllib.parse import quote_plus
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI Config Server")
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    # secrets.token_urlsafe(32) or base64.b64encode(os.urandom(32))
    SECRET_KEY: str = os.getenvb(b"SECRET_KEY", b'CyTGYUixdNilshsVY4ediB4S6HNmhf3LVDLeZxYJUD4')
    # 60 minutes * 24 hours * 8 days = 8 days = 11520 minutes 60 * 24 * 8
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS", [])

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DB_SCHEME: str = os.getenv("DB_SCHEME", "mysql")
    DB_HOST: str = os.getenv("DB_HOST", "192.168.1.34")
    DB_PROT: str = os.getenv("DB_PROT", 3306)
    DB_USER: str = os.getenv("DB_USER", "tiangong")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "TianGong@4321")
    DB_NAME: str = os.getenv("DB_NAME", "tiangong")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", None)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        db_scheme = values.get('DB_SCHEME')
        if db_scheme == "sqlite":
            return f"sqlite:///{values.get('DB_NAME')}.db"
        elif db_scheme == "mysql":
            return f"mysql+pymysql://{values.get('DB_USER')}:{quote_plus(values.get('DB_PASSWORD'))}" \
                   f"@{values.get('DB_HOST')}:{values.get('DB_PROT')}/{values.get('DB_NAME')}"
        else:
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("DB_USER"),
                password=quote_plus(values.get("DB_PASSWORD")),
                host=values.get("DB_HOST"),
                path=f"/{values.get('DB_NAME') or ''}",
            )

    FIRST_SUPERUSER: EmailStr = os.getenv("EMAIL_TEST_USER", "dage@qq.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "Abcd@4321")
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
