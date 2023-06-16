# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 14:52
# @Author  : Jieay
# @File    : health.py
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/health/check")
async def health_check():
    logger.info("Health check success.")
    return {"resultCode": 0, "errorMsg": "", "data": None}
