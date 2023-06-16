# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 11:20
# @Author  : Jieay
# @File    : deps.py
"""
在FastAPI中，"deps"（或"dependencies"）是指依赖项（Dependencies）。依赖项是指在执行某个函数或处理请求之前需要满足的条件或依赖关系。
它可以用于验证用户身份、获取数据库连接、进行权限检查等各种任务。

FastAPI提供了Depends装饰器来定义依赖项，并将其应用于需要依赖项的函数或路由上。Depends装饰器接受一个依赖项函数作为参数，用于提供依赖项的实现逻辑。
"""
import jwt

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def check_url_path_is_white(url_path) -> bool:
    """
    获取白名单
    :param url_path: url path
    :return: bool
    """
    white_list_exact = [
        "/openapi.json",
        "/login/access-token",
        "/api/access-token",
    ]
    white_list_prefix = [
        "/docs",
        "/redoc",
    ]
    if url_path in white_list_exact:
        return True
    for path in white_list_prefix:
        if url_path.startswith(path):
            return True
    return False


def get_user_from_token(token: str = Depends(reusable_oauth2)):
    """
    从token中获取用户信息
    :param token: token
    :return: user object
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        return None
    db = SessionLocal()
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        return None
    return user
