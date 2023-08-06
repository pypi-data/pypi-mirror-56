# -*- coding: utf-8 -*-
from os import path as os_path
import setuptools

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


name = 'python_terminal'
version = '1.0'
description = 'Quickly build a terminal project'
url = 'https://github.com/zhcshine/pyterminal'
mail = 'zhcshine@gmail.com'
author = 'zhuohc'


setuptools.setup(
    name=name,
    version=version,
    python_requires='>=3.4.0',
    author=author,
    author_email=mail,
    description=description,
    long_description=read_file('README.MD'),
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['pyterminal', 'terminal', '终端'],
    classifiers=(
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

# 打包
# python3 setup.py sdist bdist_wheel
