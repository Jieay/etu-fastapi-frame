# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 15:42
# @Author  : Jieay
# @File    : log_formatter.py
import uuid
import logging


"""
linux终端下输出带颜色的文字只需在文字前面添加如下格式
\033[显示方式;前景色;背景色m

显示方式	意义
0	终端默认设置
1	高亮显示
4	使用下划线
5	闪烁
7	反白显示
8	不可见

前景色	背景色	颜色
30	40	黑色
31	41	红色
32	42	绿色
33	43	黃色
34	44	蓝色
35	45	紫红色
36	46	青蓝色
37	47	白色
"""
NONE = '\033[0m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = ('\033[0;%dm' % i for i in range(30, 38))


class DefaultServerFormatter(logging.Formatter):
    """自定义日志输出格式中间件"""
    COLORS = {
        'CRITICAL': RED,
        'ERROR': RED,
        'WARNING': YELLOW,
        'INFO': GREEN,
        'DEBUG': BLUE,
    }

    def __init__(self, *args, **kwargs):
        super(DefaultServerFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        # 日志中添加一些自定义请求相关的数据
        from app.core.middleware.global_request import global_request

        record.ip = getattr(global_request, 'ip') or 'NotIp'
        record.request_id = getattr(global_request, 'request_id') or uuid.uuid4().hex[:4]
        record.user = getattr(global_request, 'user') or 'NotUser'

        # 定义linux终端下是否输出带颜色的文字
        message = super(DefaultServerFormatter, self).format(record)
        if record.levelname in self.COLORS:
            message = self.COLORS[record.levelname] + message + NONE
        return message
