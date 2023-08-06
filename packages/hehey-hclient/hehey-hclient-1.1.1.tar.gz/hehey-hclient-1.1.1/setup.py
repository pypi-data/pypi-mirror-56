# -*- coding: utf-8 -*-
import setuptools
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setuptools.setup(
    name = 'hehey-hclient',
    version = '1.1.1',
    #py_modules = ['Client','__init__','clientide'],
    #packages = ['utils','transport','protocol','format','base'],
    author = '13564768842',
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-hclient',
    description = 'hehey-hclient 是一个python 客户端请求工具组件,常用于接口的调用',
    long_description=long_description,
    long_description_content_type="text/markdown",
    )