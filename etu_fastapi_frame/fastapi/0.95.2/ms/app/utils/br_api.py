# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 12:51
# @Author  : Jieay
# @File    : br_api.py
import json
import time
import requests
import logging

from app.utils.common import random_sleep_ms

logger = logging.getLogger(__name__)


class BaseDataRequest(object):

    def __init__(self, url=None, ak=None, sk=None):
        self.API_BASE_URL = url
        self.API_BASE_AK = ak
        self.API_BASE_SK = sk
        self.headers = {'content-type': 'application/json'}

    def get_res_list(self, data):
        try:
            if data.status_code == 200:
                return data.json()
        except Exception as err:
            logger.error("调用接口异常: {}".format(err))
        return []

    def get_res_dict(self, data):
        try:
            if data.status_code == 200:
                return data.json()
        except Exception as err:
            logger.error("调用接口异常: {}".format(err))
        return {}

    def get_token(self):
        rq_url = '{}{}'.format(self.API_BASE_URL, '/api/access-token')
        data = {
            "username": self.API_BASE_AK,
            "password": self.API_BASE_SK
        }
        result = requests.post(rq_url, data=json.dumps(data))
        result = self.get_res_dict(result)
        if isinstance(result, dict):
            token = result.get('access_token')
            if token:
                self.headers['Authorization'] = 'Bearer {}'.format(token)
                return True
        return False

    def retry(*args, **wkwargs):
        """调用接口异常重试功能"""
        def warpp(func):
            def inner(self, *args, **kwargs):
                res_code = [200, 201]
                res_data = {}
                tries = wkwargs.get('tries', 3)
                delay = wkwargs.get('delay', 1)
                func_type = wkwargs.get('func_type', '')
                # 不传或者为空则默认重试3次
                if not tries:
                    tries = 3
                # 不传或者为空则默认 2 秒
                if not delay:
                    delay = 1
                number = 0
                tag = True
                while tag:
                    try:
                        random_sleep_ms()
                        res = func(self, *args, **kwargs)
                        if res.status_code in res_code:
                            res_data['data'] = res.json()
                            tag = False
                        else:
                            number += 1
                            logger.info("在{} 秒后尝试第:{}次 重试".format(delay, number))
                            logger.error("调用{}接口异常，status_code: {}".format(func_type, res.status_code))
                            time.sleep(delay)

                    except Exception as err:
                        number += 1
                        logger.info("在{} 秒后尝试第:{}次 重试".format(delay, number))
                        logger.error("调用{}接口异常: {}".format(func_type, err))
                        time.sleep(delay)

                    if number >= tries and tag is True:
                        res_data['code'] = 500
                        res_data['msg'] = 'The request is got lost.'
                        res_data['data'] = []
                        tag = False
                return res_data
            return inner
        return warpp

    @retry()
    def get(self, url, params=None, **kwargs):
        self.get_token()
        rq_url = '{}{}'.format(self.API_BASE_URL, url)
        headers = kwargs.get('headers', {})
        if isinstance(headers, dict):
            self.headers.update(headers)
        return requests.get(rq_url, params, headers=self.headers, **kwargs)

    def post(self, url, data=None, json=None, params=None, **kwargs):
        self.get_token()
        rq_url = '{}{}'.format(self.API_BASE_URL, url)
        headers = kwargs.get('headers', {})
        if isinstance(headers, dict):
            self.headers.update(headers)
        return requests.post(rq_url, data=data, json=json, headers=self.headers, params=params, **kwargs)

    def put(self, url, data=None, json=None, params=None, **kwargs):
        self.get_token()
        rq_url = '{}{}'.format(self.API_BASE_URL, url)
        headers = kwargs.get('headers', {})
        if isinstance(headers, dict):
            self.headers.update(headers)
        return requests.put(rq_url, data=data, json=json, headers=self.headers, params=params, **kwargs)

    def delete(self, url, data=None, json=None, params=None, **kwargs):
        self.get_token()
        rq_url = '{}{}'.format(self.API_BASE_URL, url)
        headers = kwargs.get('headers', {})
        if isinstance(headers, dict):
            self.headers.update(headers)
        return requests.delete(rq_url, data=data, json=json, headers=self.headers, params=params, **kwargs)
