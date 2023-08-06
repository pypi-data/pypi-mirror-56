#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2010 Joachim Hoessler <hoessler@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


from setuptools import setup

setup(
    name='TracEstimationTools',
    author='Joachim Hoessler',
    author_email='hoessler@gmail.com',
    description='Trac plugin for visualizing and quick editing of effort '
                'estimations',
    version='0.5.0',
    license='BSD',
    url='https://trac-hacks.org/wiki/EstimationToolsPlugin',
    packages=['estimationtools'],
    package_data={'estimationtools': ['htdocs/*.js', 'templates/*.html']},
    classifiers=['Framework :: Trac'],
    entry_points={
        'trac.plugins': [
            'estimationtools = estimationtools'
        ]
    },
    install_requires=['Trac'],
    test_suite='estimationtools.tests.test_suite',
    tests_require=[]
)
