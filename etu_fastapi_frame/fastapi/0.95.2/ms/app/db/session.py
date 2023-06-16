# -*- coding: utf-8 -*-
# @Time    : 2023/6/13 16:06
# @Author  : Jieay
# @File    : session.py
import os
import json
import base64
from app.utils.common import check_json_format
from app.core.config import settings


class SessionLocal:
    def __init__(self, db_name='db_user'):
        self.db_name = db_name
        self._db_file = os.path.join(self.root_dir(), f'{self.db_name}.json')
        self.__debug_file = os.path.join(self.root_dir(), f'{self.db_name}_debug.json')

    def root_dir(self):
        return os.path.dirname(__file__)

    def base64_encode(self, data):
        """
        base64编码
        :param data: str 即: json.dumps
        :return: str 即: base64
        """
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def base64_decode(self, data):
        """
        base64解码
        :param data: str 即: base64
        :return: str 即: json.dumps
        """
        return base64.b64decode(data.encode('utf-8')).decode('utf-8')

    def read_databases_decode(self, data):
        """
        读取数据库时，对数据进行base64解码
        :param data: object
        :return: object
        """
        try:
            db_databases = data.get('databases')
            databases = self.base64_decode(db_databases)
            if check_json_format(databases):
                databases = json.loads(databases)
            data['databases'] = databases
            return data
        except Exception as e:
            return data

    def write_databases_encode(self, data):
        """
        写入数据库时，对数据进行base64编码
        :param data: object
        :return: str
        """
        try:
            db_databases = data.get('databases')
            if not check_json_format(db_databases):
                db_databases = json.dumps(db_databases)
            databases = self.base64_encode(db_databases)
            data['databases'] = databases
            return data
        except Exception as e:
            return data

    def read_json(self, file_path):
        """
        读取json文件
        :param file_path: 数据库文件路径，例如: /app/db/db_user.json
        :return: object
        """
        with open(file_path, 'r') as f:
            json_data = f.read()
        if check_json_format(json_data):
            db_data = json.loads(json_data)
            return self.read_databases_decode(db_data)
        return None

    def write_json(self, file_path, data, encode=True):
        """
        写入json文件
        :param file_path: 数据库文件路径，例如: /app/db/db_user.json
        :param data: object
        :param encode: bool 是否对数据进行base64编码
        """
        with open(file_path, 'w') as f:
            if encode:
                db_data = self.write_databases_encode(data)
                json.dump(db_data, f, indent=2)
            else:
                json.dump(data, f, indent=2)

    def get_databases(self):
        """
        获取数据库
        :return: object [{}, {}]
        """
        db_data: dict = {}
        if os.path.exists(self._db_file):
            json_data = self.read_json(self._db_file)
            if isinstance(json_data, dict):
                db_data.update(json_data)
        _database = []
        if db_data.get('databases', []):
            _database.extend(db_data.get('databases', []))
        return _database

    def up_db_data(self, data, db_file=None, encode=True):
        """
        更新数据库数据
        :param data: object [{}, {}]
        :param db_file: 数据库文件路径，例如: /app/db/db_user.json
        :param encode: bool 是否对数据进行base64编码
        """
        db_data: dict = {}
        if db_file is None:
            db_file = self._db_file
        if os.path.exists(db_file):
            json_data = self.read_json(db_file)
            if isinstance(json_data, dict):
                db_data.update(json_data)
        version = db_data.get('version', 1)
        _database = db_data.get('databases', [])
        # 将数据替换原来本地的 databases 字典数据
        if isinstance(data, list):
            _database = data
        db_data['name'] = self.db_name
        db_data['version'] = version + 1
        db_data['databases'] = _database
        self.write_json(db_file, db_data, encode)

    def data_encode(self):
        """
        数据库数据加密
        """
        databases = self.get_databases()
        self.up_db_data(databases)

    def debug_decode_data(self):
        """
        调试数据, 用于测试
        """
        if settings.LOG_LEVEL.lower() == 'debug':
            databases = self.get_databases()
            self.up_db_data(data=databases, db_file=self.__debug_file, encode=False)
