# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 16:21
# @Author  : Jieay
# @File    : main.py

import uvicorn
import logging.config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import api_router
from app.core.config import settings
from app.core.log import CustomLogConfig
from app.core.middleware.global_request import GlobalRequestMiddleware
from app.core.middleware.global_authorized import GlobalAuthorizedMiddleware
from app.db.sync_org_user import SyncOrgUser

app = FastAPI(title=settings.PROJECT_NAME)

# 新增模块注册日志
loggers_app = [
    "fastapi",
    "uvicorn",
    "app",
]
LOGGING = CustomLogConfig().set_logging(settings.LOG_LEVEL, loggers_app)
logging.config.dictConfig(LOGGING)

# 创建日志记录器
logger = logging.getLogger(__name__)

# 将中间件添加到应用中
app.add_middleware(GlobalRequestMiddleware)
app.add_middleware(GlobalAuthorizedMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

# 同步用户
SyncOrgUser().sync_user()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8052, reload=True, log_level="info")

