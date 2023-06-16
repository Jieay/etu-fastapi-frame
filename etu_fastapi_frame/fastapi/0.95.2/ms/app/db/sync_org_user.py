# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 15:13
# @Author  : Jieay
# @File    : sync_org_user.py
import logging
from app.db.session import SessionLocal
from app.utils.orgauth import OrgauthDataManager

logger = logging.getLogger(__name__)


class SyncOrgUser(object):

    def __init__(self):
        self.db = SessionLocal(db_name='db_user')
        self.orgauth = OrgauthDataManager()

    def sync_user(self):
        """
        同步用户
        :return:
        """
        user_list = self.orgauth.get_user_list()
        if user_list:
            self.db.up_db_data(data=user_list)
            logger.info('同步用户成功')
            logger.info(f'同步用户数据总计: {len(user_list)}')
            return True
        return False
