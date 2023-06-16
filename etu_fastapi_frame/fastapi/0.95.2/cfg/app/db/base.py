# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:40
# @Author  : Jieay
# @File    : base.py

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa

