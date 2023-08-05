#!/usr/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Hanyu
# Mail: hanyuzhang94@bupt.edu.cn
# Created Time:  2019-7-23 19:17:34
#############################################
from os import path as os_path
from setuptools import setup, find_packages
this_directory = os_path.abspath(os_path.dirname(__file__))
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
setup(
    name = "hanyutools",
    version = "0.1.4",
    keywords = ("pip", "hanyutools", "hanyu"),
    description = " tool edited by hanyu",
    long_description = "some tool",
    license = "Hanyu Licence",

    url = "https://github.com/DruidHanyu",
    author = "Hanyu",
    author_email = "zhanghanyu94@bupt.edu.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)

