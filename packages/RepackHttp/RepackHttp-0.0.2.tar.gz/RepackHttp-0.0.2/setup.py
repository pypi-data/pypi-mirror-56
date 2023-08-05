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
import os

curdir = os.path.curdir

with open(os.path.join(curdir, "README.md"), "r", encoding="utf8", errors="ignore") as fh:
    long_description = fh.read()



install_packages = [
'certifi==2019.9.11',
'chardet==3.0.4',
'idna==2.8',
'lxml==4.4.1',
'requests==2.22.0',
'urllib3==1.25.7',
]

setuptools.setup(
    name="RepackHttp",
    version="0.0.2",
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
