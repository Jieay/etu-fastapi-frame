# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 17:10
# @Author  : Jieay
# @File    : config.py
import os
# import base64
# import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI MS")
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
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

    # 配置权限中心
    ORGAUTH_SERVER_URL: str = os.getenv("ORGAUTH_SERVER_URL", "http://localhost:8051")
    ORGAUTH_SERVER_AK: str = os.getenv("ORGAUTH_SERVER_AK", "dage@qq.com")
    ORGAUTH_SERVER_SK: str = os.getenv("ORGAUTH_SERVER_SK", "Abcd@4321")

    class Config:
        case_sensitive = True


settings = Settings()
