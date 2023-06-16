# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 17:42
# @Author  : Jieay
# @File    : user.py

from app.db.base import BaseManager
from app import schemas


class User(BaseManager):

    DB_NAME = 'db_user'

    def get_schemas_user(self, data):
        if data:
            return schemas.UserInDB(**data)
        return None
