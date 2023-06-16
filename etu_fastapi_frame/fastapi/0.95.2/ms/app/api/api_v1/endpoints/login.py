# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 18:19
# @Author  : Jieay
# @File    : login.py
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.user import User

router = APIRouter()


@router.post("/api/access-token", response_model=schemas.Token)
def login_access_token(form_data: schemas.GetToken) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    json_data = form_data.dict()
    username = json_data.get("username")
    password = json_data.get("password")
    email = username
    user_info = User().query_first(email=email).first()
    user = User().get_schemas_user(user_info)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not security.verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: schemas.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Test access token
    """
    return current_user

