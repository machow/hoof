#!/usr/bin/env python

import re
import ast
from setuptools import setup, find_namespace_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('hoof.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='hoof',
    version=version,
    py_modules=['hoof'],
    packages=find_namespace_packages(include="hoof_examples.*"),
    install_requires=[
        'antlr4-python3-runtime>=4.7.2',
        'siuba'
        ],
    description='Generate abstract syntax trees using antlr grammars',
    author='Michael Chow',
    author_email='mc_al_github@fastmail.com',
    url='https://github.com/machow/hoof'
    )
