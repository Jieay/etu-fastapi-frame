# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 15:16
# @Author  : Jieay
# @File    : global_authorized.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.deps import get_current_user, check_url_path_is_white


class GlobalAuthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 在请求之前执行的逻辑
            # 可以在这里进行请求处理、验证、日志记录等操作
            if not check_url_path_is_white(request.url.path):
                authorization_str = request.headers.get("Authorization")
                # Bearer eyJhbGciOiJIU.sSd2WS.Wcs2d
                if not authorization_str:
                    # 验证 token 是否存在
                    raise HTTPException(status_code=401, detail="Unauthorized")
                # 验证 token 是否有效
                token = authorization_str.split(" ")[-1]
                user = get_current_user(token)
                if not user:
                    raise HTTPException(status_code=401, detail="Unauthorized")

            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": e.detail})
