# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 22:43
# @Author  : Jieay
# @File    : routers.py
from fastapi import APIRouter
from .core.config import settings
from app.api.api_v1.api import api_v1_router
from app.api.api_v1.endpoints import login, health


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(api_v1_router, prefix=settings.API_V1_STR)
