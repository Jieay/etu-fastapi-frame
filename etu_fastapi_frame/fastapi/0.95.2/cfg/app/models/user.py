# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 22:50
# @Author  : Jieay
# @File    : user.py
from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), index=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
