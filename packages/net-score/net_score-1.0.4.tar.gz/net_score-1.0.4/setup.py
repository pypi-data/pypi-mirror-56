#!/usr/bin/env python3.7
# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='net_score',
    version='1.0.4',
    description=(
        '网络人物画像'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kyo',
    author_email='mytool2002@126.com',
    maintainer='kyo',
    maintainer_email='mytool2002@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pyecharts>=1.5.1',
    ]
)
