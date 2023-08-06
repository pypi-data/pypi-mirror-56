from setuptools import setup
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))
# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
	name='fdfs_client_py34',
	python_requires='>=3.4.0',
	version='0.1',
	description='The fdfs_client package for python3',
	packages=['fdfs_client'],
	long_description=read_file('README.md'), # 读取的Readme文档内容
	author="greybeetle", # 作者相关信息
    author_email='hanxuan_g@163.com',
    url='https://github.com/Greybeetle/My_Pypi',
	zip_safe=False
	)
	
	
	
	