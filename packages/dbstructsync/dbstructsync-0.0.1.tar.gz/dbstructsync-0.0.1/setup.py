#-*-coding:utf-8-*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# 配置项比较多，有些不是必须，可参考官方文档 https://packaging.python.org/guides/distributing-packages-using-setuptools/
setuptools.setup(
    name="dbstructsync", # 项目的名字，将来通过pip install dbstructsync安装，不能与其他项目重复，否则上传失败
    version="0.0.1", # 项目版本号，自己决定吧
    author="yingchen_double_1", # 作者
    author_email="a860608@126.com", # email
    description="同步mysql多套环境的数据库表结构及索引",  # 项目描述
    long_description=long_description, # 加载read_me的内容
    long_description_content_type="text/markdown", # 描述文本类型
    url="",  # 项目的地址，比如github或者gitlib地址
    packages=setuptools.find_packages(),  # 这个函数可以帮你找到包下的所有文件，你可以手动指定
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # 该软件包仅与Python 3兼容，根据MIT许可证进行许可，并且与操作系统无关。您应始终至少包含您的软件包所使用的Python版本，软件包可用的许可证以及您的软件包将使用的操作系统。有关分类器的完整列表，请参阅 https://pypi.org/classifiers/。
    install_requires=[
        'argparse',
        'pymysql',
        'pyyaml',
    ], # 项目依赖，也可以指定依赖版本
)
