# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 18:25
# @Author  : Jieay
# @File    : base.py

from app.db.session import SessionLocal


class BaseManager:

    DB_NAME = None

    def __init__(self):
        self._first = {}

    def get_db(self):
        return SessionLocal(db_name=self.DB_NAME)

    def is_subset(self, subset, superset):
        return subset.items() <= superset.items()

    def get_sub_info_list(self, term, data_list):
        return [x for x in data_list if self.is_subset(term, x)]

    def query_filter(self, **kwargs):
        data = self.get_db().get_databases()
        if isinstance(kwargs, dict):
            return self.get_sub_info_list(kwargs, data)
        return []

    def query_first(self, **kwargs):
        _query_filter = self.query_filter(**kwargs)
        if _query_filter:
            self._first.update(_query_filter[0])
        return self

    def first(self):
        return self._first

