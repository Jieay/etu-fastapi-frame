# -*- coding: utf-8 -*-
# @Time    : 2023/6/5 10:28
# @Author  : Jieay
# @File    : api.py
from fastapi import APIRouter

from app.api.api_v1.endpoints import users


api_v1_router = APIRouter()
# api_v1_router.include_router(login.router, tags=["login"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
