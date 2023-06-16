# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 15:48
# @Author  : Jieay
# @File    : common.py
import jwt
import json
import time
import random
from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    """生成密码重置token"""
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """验证密码重置token"""
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.PyJWTError:
        return None


def check_json_format(json_str):
    """检查json格式"""
    try:
        json.loads(json_str)
    except Exception as e:
        return False
    return True


class NewSetDictToObj:
    """将字典转换为对象"""
    def __init__(self, data):
        self.__dict__.update(data)


def random_sleep_ms():
    """随机毫秒休眠"""
    sleep_time = random.randint(0, 100) * 0.01
    time.sleep(sleep_time)
    return sleep_time
