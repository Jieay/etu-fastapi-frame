# -*- coding: utf-8 -*-
# @Time    : 2023/6/9 10:17
# @Author  : Jieay
# @File    : global_request.py
import uuid
import threading
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.common import NewSetDictToObj
from app.api.deps import get_user_from_token


# 创建一个 threading.local() 对象
threading_local = threading.local()


class GlobalRequestMiddleware(BaseHTTPMiddleware):

    # 自定义中间件逻辑
    async def dispatch(self, request: Request, call_next):
        # 在请求之前执行的逻辑
        # 可以在这里进行请求处理、验证、日志记录等操作
        # 获取客户端 IP 地址
        client_ip = request.client.host
        # 获取请求用户
        user = "UnknownUser"  # 设置默认用户
        authorization_str = request.headers.get("Authorization")
        if authorization_str:
            token = authorization_str.split(" ")[-1]
            user_obj = get_user_from_token(token)
            if user_obj:
                user = user_obj.name

        # 将客户端 IP 地址和用户信息添加到日志记录的上下文中
        request_info = {
            "ip": client_ip,
            "user": user,
            "request_id": self.generate_request_id(),
        }
        # 存储请求信息字段值到 threading.local() 对象中
        threading_local.request_info = request_info

        response = await call_next(request)

        # 在响应之后执行的逻辑
        # 可以在这里进行响应处理、日志记录等操作

        return response

    @staticmethod
    def generate_request_id():
        return uuid.uuid4().hex[:4]


class GlobalRequest:

    def __getattr__(self, item):
        request_info = getattr(threading_local, 'request_info', {})
        return getattr(NewSetDictToObj(request_info), item, None)


global_request = GlobalRequest()

