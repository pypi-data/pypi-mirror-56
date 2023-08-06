#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xxzlib
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "xxzlib",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "FAIH","xxzlib"),
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
    license = "MIT Licence",
    author = "sniper",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
)

