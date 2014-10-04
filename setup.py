#!/usr/bin/env python

import glob
from setuptools import setup

requires = [
    'tornado',
    ]

setup(
    name='miura',
    version='0.1.0',
    description='MIURA: pattern matcher for morpheme sequences',
    author='Yuya Unno',
    author_email='unnonouno@gmail.com',
    url='https://github.com/unnonouno/miura',
    packages=['miura',
              ],
    package_data={
        'miura': [
            'template/*.html',
            'static/css/*.css',
            'static/css/*.png',
            'static/img/*.png',
            'static/img/*.jpg',
            'static/js/*.js',
            ]
        },
    scripts=[
        'command/miuraserver',
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

