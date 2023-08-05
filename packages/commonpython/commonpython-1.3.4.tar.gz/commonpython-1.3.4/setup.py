#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@file: setup.py
@time: 2018/10/24
发布命令：
    python3 setup.py sdist bdist_wheel
    twine upload dist/*
	
	username: xchen2
	password:Xuc13381015
	
	登录网站：  https://pypi.org/manage/projects/
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commonpython",
    version="1.3.4",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

