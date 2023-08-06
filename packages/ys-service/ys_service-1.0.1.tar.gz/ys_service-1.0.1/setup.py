#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 17:37
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : setup.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
import setuptools

with open("README.md", "r") as f:
    detail_description = f.read()

with open("requirements.txt", "r") as f:
    requirement = f.read().split("\n")


setuptools.setup(
    name="ys_service",
    version="1.0.1",
    author="7913",
    author_email="84328409@qq.com",
    description="云上host,python版",
    long_description=detail_description,
    long_description_content_type="text/markdown",
    install_requires=requirement,
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
