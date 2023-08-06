#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: DAHANGZAIYA
# Mail: y17505251998@163.com
# Created Time:  2019-11-28 22:22:22
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="OAuthWb",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "SICA", "featureextraction"),
    description="An feature extraction algorithm",
    long_description="An feature extraction algorithm, improve the FastICA",
    license="MIT Licence",

    author="DAHANGZAIYA",
    author_email="y17505251998@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["json", "requests"]  # 这个项目需要的第三方库
)
