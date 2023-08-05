#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

import west_ishara

project_dir = os.path.dirname(os.path.realpath(__file__))
requirement_file_path = project_dir + '/requirements.txt'
requirements = []
if os.path.isfile(requirement_file_path):
    with open(requirement_file_path) as f:
        requirements = f.read().splitlines()

setup(
    name=west_ishara.__name__,
    version=west_ishara.__version__,
    author=west_ishara.__author__,
    author_email=west_ishara.__author_email__,
    url='https://bitbucket.org/tncy/my-project2/',
    description='A sample project.',
    long_description=open('README.rst').read(),
    license="Apache License, Version 2.0",

    packages=find_packages(exclude=['tests', 'data']),
    include_package_data=True,
    install_requires=requirements,

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Education'
    ]
)
