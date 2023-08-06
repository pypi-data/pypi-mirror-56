# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# 如果没有setuptools的话，就用distutils.core的setup
# package_data = {'nn_test': ['img/example.jpg','a.txt']} #把要上传的其他目录下的文件，放到这个list里面

# 下面的代码是自动的找项目下面的其他资源放到resources里面
name = 'yamail'
version = '1.0.0'
description = '发送电子邮件的模块，源码99%是yagmail里面的，稍微改了一点东西。'
resources = []
for dirpath, dirnames, filenames in os.walk(name):
    for file in filenames:
        if dirpath == name:  # 如果是当前项目目录的话
            if not file.endswith('.py'):  # 不取py文件，因为python文件不是其他资源，是程序
                resources.append(file)
        else:
            basepath = dirpath.split(os.path.sep, 1)[1]  # nn_test/img路径是这样，取img
            resources.append(os.path.join(basepath, file))  # 拼好的路径就是img/example.jpg

package_data = {name: resources}

setup(
    name=name,  # 模块的名称
    version=version,  # 版本号，每次修改代码的时候，可以改一下
    description=description,  # 描述
    author="牛牛",  # 作者
    author_email="niuhanyang@163.com",  # 联系邮箱
    url="http://www.nnzhp.cn",  # 你的主页
    packages=[name, ],  # 指定哪个包，会自动的找这个文件夹下面的python文件
    package_data=package_data  # 这个如果目录下有一些文件夹，其他的资源需要上传的话
)
