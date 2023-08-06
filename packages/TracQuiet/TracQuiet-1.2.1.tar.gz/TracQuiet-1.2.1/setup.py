#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2012 Rob Guttman <guttman@alum.mit.edu>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from setuptools import setup, find_packages

PACKAGE = 'TracQuiet'
VERSION = '1.2.1'

setup(
    name=PACKAGE,
    version=VERSION,
    description='Toggles quiet (no email) mode for Trac notifications',
    author="Rob Guttman",
    author_email="guttman@alum.mit.edu",
    license='3-Clause BSD',
    url='https://trac-hacks.org/wiki/QuietPlugin',
    install_requires=['Trac'],
    packages=['quiet'],
    package_data={'quiet': ['htdocs/*.js', 'htdocs/*.css', 'htdocs/*.png']},
    classifiers=['Framework :: Trac'],
    entry_points={'trac.plugins': ['quiet.web_ui = quiet.web_ui']}
)
