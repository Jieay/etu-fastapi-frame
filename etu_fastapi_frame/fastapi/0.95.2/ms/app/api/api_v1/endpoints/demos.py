# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 12:08
# @Author  : Jieay
# @File    : demos.py
import logging
from fastapi import APIRouter


logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/")
async def get_demos():
    logger.info("get_demos")
    return {"msg": "get_demos"}


@router.post("/")
async def post_demos():
    logger.info("post_demos")
    return {"msg": "post_demos"}


@router.put("/")
async def put_demos():
    logger.info("put_demos")
    return {"msg": "put_demos"}


@router.delete("/")
async def delete_demos():
    logger.info("delete_demos")
    return {"msg": "delete_demos"}

