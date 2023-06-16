# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 14:20
# @Author  : Jieay
# @File    : demos.py
from enum import Enum
from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"