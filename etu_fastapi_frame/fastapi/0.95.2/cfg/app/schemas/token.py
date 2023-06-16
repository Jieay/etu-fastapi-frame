# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:52
# @Author  : Jieay
# @File    : token.py
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class GetToken(BaseModel):
    username: str
    password: str
