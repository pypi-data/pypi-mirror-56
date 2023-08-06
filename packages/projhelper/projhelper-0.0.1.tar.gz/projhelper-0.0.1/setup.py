#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19/11/26 11:23
# @Author  : oujianhua
# @mail  : ojhtyy@163.com
# @File    : setup.py
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name = "projhelper",
    version = "0.0.1",
    keywords = ("pip", "datacanvas", "eds", "xiaoh"),
    description = "eds sdk",
    long_description = "eds sdk for python",
    license = "MIT Licence",

    url = "http://xiaoh.me",
    author = "xiaoh",
    author_email = "huoxingming@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)