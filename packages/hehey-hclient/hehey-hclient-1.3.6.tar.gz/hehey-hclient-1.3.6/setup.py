# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setup(
    name = 'hehey-hclient',
    version = '1.3.6',
    author = '13564768842',
    packages=find_packages(),
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-hclient',
    description = 'hehey-hclient 是一个python 客户端请求工具组件,常用于接口的调用',
    long_description=long_description,
    long_description_content_type="text/markdown",
)