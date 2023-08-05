#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
'''

 * @version: 0.0.0
 * @Company: 
 * @Author: zhanming.zhang 
 * @Date: 2019/11/16 16:56 
 * @Last Modified by:   zhanming.zhang 
 * @Last Modified time: 2019/11/16 16:56
 * @Desc: 
'''
import setuptools

with open("README.md", "r", encoding="utf8", errors="ignore") as fh:
    long_description = fh.read()


with open("requirements.txt", "r") as fh:
    install_packages = fh.readlines()

setuptools.setup(
    name="RepackHttp",
    version="0.0.1",
    author="Zhang Zhanming",
    author_email="chinming95@foxmail.com",
    description="RepackHttp packet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cchinm/RepackHttp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
    install_requires=install_packages,
)
