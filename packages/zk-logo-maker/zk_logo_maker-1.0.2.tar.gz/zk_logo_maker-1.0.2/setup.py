#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: JeffreyCao
# Mail: jeffreycao1024@gmail.com
# Created Time:  2019-11-16 21:48:34
#############################################

# from setuptools import setup, find_packages  # 这个包没有的可以pip一下
import setuptools

setuptools.setup(
    name="zk_logo_maker",
    version="1.0.2",
    keywords=("pip", "zk_logo_maker"),
    description="Tool to make zhike logos",
    long_description="Tool to make zhike logos",
    license="MIT Licence",

    url="https://github.com/caojianfeng/zk_logo_maker",  # 项目相关文件地址，一般是github
    author="JeffreyCao",
    author_email="jeffreycao1024@gmail.com",

    packages=setuptools.find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["Pillow"],  # 这个项目需要的第三方库

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
