#!/usr/bin/env python

import os
from setuptools import setup

requires = [
    'mecab-python3',
    ]

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='miura',
    version='0.1.0',
    description='MIURA: pattern matcher for morpheme sequences',
    long_description=read('README.rst'),
    author='Yuya Unno',
    author_email='unnonouno@gmail.com',
    url='https://github.com/unnonouno/miura',
    packages=['miura',
              ],
    scripts=[
        'command/miura',
    ],
    install_requires=requires,
    license='MIT',
    test_suite='test',
    classifiers = [
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
    ],
    )

