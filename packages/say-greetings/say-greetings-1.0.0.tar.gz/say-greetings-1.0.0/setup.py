# MIT
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://bitbucket.org/gurpreet-anand/say-greetings/src/master/say-greetings/
# Filename: setup.py
# Description: Setup for `say_greetings` package

from setuptools import setup, find_packages

long_description = 'Simple python package to greet a person'

setup(
    name='say-greetings',
    version='1.0.0',
    author='Gurpreet Anand',
    author_email='gurpreetsinghanand@live.com',
    url='',
    description='A simple command-line app to greet!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'greetings=say_greetings.greetings:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='greetings say_greetings python package gurpreetsinghanand Gurpreet Anand',
    zip_safe=False
)
