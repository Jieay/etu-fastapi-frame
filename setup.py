#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/17 15:22
# @Author  : Jieay
# @File    : setup.py

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools


setup(
    name='etu-fastapi-frame',  # 包的名字
    version='1.3.1',  # 版本号
    author="Jieay",
    author_email="1016900854@qq.com",
    description='将EFF脚手架工具，制作成为pip安装包，以方便使用',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    packages=setuptools.find_packages(),  # 包需要引用的文件夹
    # packages = setuptools.find_packages(exclude=['文件夹名字']),
    include_package_data=True,

    # 依赖包, 应用到的第三方库
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'eff-admin = etu_fastapi_frame.main:execute_from_command_line',
        ],
    },
)