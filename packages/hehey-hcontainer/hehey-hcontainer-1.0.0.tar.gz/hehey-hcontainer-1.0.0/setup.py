# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("./README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name = 'hehey-hcontainer',
    version = '1.0.0',
    author = '13564768842',
    packages=find_packages(),
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-hcontainer',
    description = 'hehey-hcontainer 是一个python di 容器,提供依赖注入等等功能',
    long_description=long_description,
    long_description_content_type="text/markdown",
)