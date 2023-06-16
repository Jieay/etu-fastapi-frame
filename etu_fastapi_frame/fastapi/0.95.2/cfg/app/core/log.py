# -*- coding: utf-8 -*-
# @Time    : 2023/6/9 10:09
# @Author  : Jieay
# @File    : log.py


class CustomLogConfig:
    """全局日志格式定义"""

    def get_logging(self, level):
        # settings LOGGING
        logging = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s [%(asctime)s] %(pathname)s %(lineno)d %(funcName)s %(process)d '
                              '%(thread)d \n \t %(message)s \n',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'main': {
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                    'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
                },
                'simple': {
                    "()": "app.core.middleware.log_formatter.DefaultServerFormatter",
                    'format': "[%(levelname)s %(asctime)s %(process)d %(name)s %(module)s:%(lineno)d] %(message)s",
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'msg': {
                    'format': '%(message)s'
                },
                "custom": {
                    # 使用自定义日志输出格式中间件
                    "()": "app.core.middleware.log_formatter.DefaultServerFormatter",
                    "format": "%(levelname)1.1s [%(process)s-%(request_id)s %(asctime)s %(user)s "
                              "%(name)s|%(module)s:%(lineno)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            'handlers': {
                "console": {
                    "level": level,
                    "class": "logging.StreamHandler",
                    # "formatter": 'simple',
                    # "formatter": 'verbose',
                    "formatter": 'custom',
                    "stream": "ext://sys.stdout"
                }
            },
            'loggers': {
                "app": {
                    "level": level,
                    "handlers": ["console"],
                    "propagate": False
                },
            }
        }
        return logging

    def set_logging(self, level, loggers_app):
        logging = self.get_logging(level)

        loggers_comm = {
            "level": level,
            "handlers": ["console"],
            "propagate": False
        }

        for log_app in loggers_app:
            logging['loggers'][log_app] = loggers_comm

        return logging
