# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 11:20
# @Author  : Jieay
# @File    : deps.py
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError

from app import schemas
from app.core import security
from app.core.config import settings
from app.db.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)


def get_current_user(token: str = Depends(reusable_oauth2)):
    """
    检查当前用户
    :param token: token
    :return: user object
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )

    user_info = User().query_first(id=token_data.sub).first()
    user = User().get_schemas_user(user_info)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """
    检查当前用户是否是激活状态
    :param current_user: user object
    :return: user object
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user.")
    return current_user


def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """
    检查当前用户是否是超级用户
    :param current_user: user object
    :return: user object
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges."
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
        "/api/access-token",
        "/health/check",
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

    user_info = User().query_first(id=token_data.sub).first()
    user = User().get_schemas_user(user_info)
    if not user:
        return None
    return user
