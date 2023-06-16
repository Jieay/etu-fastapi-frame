# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:52
# @Author  : Jieay
# @File    : msg.py
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str
