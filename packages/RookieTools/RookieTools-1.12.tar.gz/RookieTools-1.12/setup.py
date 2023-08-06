#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

# 引用包管理工具setuptools，其中find_packages可以帮我们便捷的找到自己代码中编写的库
from setuptools import setup, find_packages

setup(
    name='RookieTools',  # 包名称，之后如果上传到了pypi，则需要通过该名称下载
    version='1.12',  # version只能是数字，还有其他字符则会报错
    keywords=('setup', 'RookieTools'),
    description='setup RookieTools',
    long_description='',
    license='MIT',  # 遵循的协议
    install_requires=['requests', 'lxml', 'chardet', 'tldextract', 'urllib3', 'IPy'],  # 这里面填写项目用到的第三方依赖
    author='Rookie',
    author_email='hyll8882019@outlook.com',
    platforms='any',
    url='https://github.com/hyll8882019/RookieTools',  # 项目链接
    include_package_data=True,
    packages=find_packages(
        'src',
        exclude=[  # 过滤不需要的代码
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests"
        ]),  # 包含所有src中的包
    package_dir={'': 'src'},  # 告诉distutils包都在src下
    package_data={
        # 任何包中含有.txt文件，都包含它
        # '': ['*.txt'],
        # 包含demo包data文件夹中的 *.dat文件
        # 'demo': ['data/*.dat'],
    },
)
