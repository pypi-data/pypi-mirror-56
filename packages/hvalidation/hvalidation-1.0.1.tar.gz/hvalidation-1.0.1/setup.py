# -*- coding: utf-8 -*-
import setuptools
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

#python3.6 setup.py sdist upload

setuptools.setup(
    name = 'hvalidation',
    version = '1.0.1',
    author = '13564768842',
    author_email = 'chinabluexfw@163.com',
    url = 'https://gitee.com/chinahehe/hehey-hvalidation',
    description = 'hehey-hvalidation 是一个python 全面的验证器工具类.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    )