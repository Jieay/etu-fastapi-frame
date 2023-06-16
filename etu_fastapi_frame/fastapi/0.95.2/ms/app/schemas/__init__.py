# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 10:45
# @Author  : Jieay
# @File    : __init__.py
"""
在 FastAPI 项目中，schemas（也称为数据模型或数据结构）用于定义请求和响应的数据结构。schemas 的作用是为 API 定义清晰的数据结构，
并提供数据验证和文档生成等功能。

使用 schemas 可以实现以下功能：

数据验证：通过定义 schemas，可以对请求数据进行验证，确保数据的类型、格式和完整性符合预期。这有助于防止无效或不完整的数据进入 API。

数据转换：schemas 可以将请求数据转换为 Python 对象，或将 Python 对象转换为响应数据。这样可以方便地对数据进行处理和操作，
        例如进行计算、过滤、格式化等操作。

自动文档生成：schemas 可以与 FastAPI 的自动文档生成工具集成，生成清晰的 API 文档。这使得开发人员和用户可以快速了解 API 的数据结构
            和字段要求，提高开发效率和交互性。

响应模型：使用 schemas，可以定义 API 的响应数据结构，使得 API 的响应结果更加规范和一致。这有助于前端开发人员更好地理解和处理 API 返回的数据。

数据序列化和反序列化：schemas 可以用于将数据从 Python 对象序列化为 JSON 或其他格式，以便在网络传输或存储中使用。反过来，schemas 也可以
                    将接收到的数据从 JSON 或其他格式反序列化为 Python 对象。

通过使用 schemas，可以明确定义 API 的数据结构和字段要求，增强代码的可读性、可维护性和健壮性。它是 FastAPI 中处理数据的重要组成部分，使得
开发者能够更加方便地处理请求和响应的数据。
"""
from .msg import Msg
from .token import Token, TokenPayload, GetToken
from .user import User, UserCreate, UserInDB, UserUpdate
