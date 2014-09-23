#!/usr/bin/env python

import glob
from setuptools import setup

requires = [
    'tornado',
    ]

setup(
    name='miura',
    version='0.1.0',
    description='MIURA',
    author='Yuya Unno',
    author_email='unnonouno@gmail.com',
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
    )

