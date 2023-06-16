# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:34
# @Author  : Jieay
# @File    : base_class.py
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
