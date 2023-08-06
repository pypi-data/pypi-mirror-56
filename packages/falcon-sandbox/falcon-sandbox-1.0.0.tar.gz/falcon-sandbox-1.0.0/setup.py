#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

__version__ = "1.0.0"
description = "Python client library and command line tool for the [Falcon Sandbox API](https://www.falcon-sandbox.com/docs/api/v2)."

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='falcon-sandbox',

    version=__version__,

    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/ace-ecosystem/falcon-sandbox',

    author='John Davison & Sean McFeely',
    author_email='mcfeelynaes@gmail.com',

    license='Apache-2.0',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Information Security,Malware Analysis',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests', 'coloredlogs'],
    entry_points={
        'console_scripts': ['falcon-sandbox=falcon_sandbox.cli:main'],
    }
)
