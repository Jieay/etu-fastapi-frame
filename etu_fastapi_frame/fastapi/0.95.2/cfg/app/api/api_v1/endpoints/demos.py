# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 12:08
# @Author  : Jieay
# @File    : demos.py
import logging

from typing import Union

from fastapi import APIRouter
from app import schemas

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


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.Item):
    return {"item_name": item.price, "item_id": item_id}


@router.get("/models/{model_name}")
async def get_model(model_name: schemas.ModelName):
    if model_name is schemas.ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
