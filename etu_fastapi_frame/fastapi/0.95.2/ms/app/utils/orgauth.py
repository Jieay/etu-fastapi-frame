# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 12:57
# @Author  : Jieay
# @File    : orgauth.py

from app.core.config import settings
from app.utils.br_api import BaseDataRequest


class OrgauthDataManager(BaseDataRequest):

    def __init__(self):
        super(OrgauthDataManager, self).__init__(
            url=settings.ORGAUTH_SERVER_URL,
            ak=settings.ORGAUTH_SERVER_AK,
            sk=settings.ORGAUTH_SERVER_SK
        )

    def get_user_list(self):
        """
        获取用户列表
        :return: [{id, name, password, email, is_active, is_superuser}}]
        """
        url = '/api/v1/users/org'
        res = self.get(url=url)
        return res.get('data', [])

