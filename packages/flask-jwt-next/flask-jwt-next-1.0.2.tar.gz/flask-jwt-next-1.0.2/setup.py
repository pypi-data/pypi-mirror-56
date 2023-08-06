#!/usr/bin/env python3

# Copyright 2014 Matthew Wright. All rights reserved.
# Copyright 2019 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.

# Forked from https://github.com/mattupstate/flask-jwt


from setuptools import setup, find_packages

from flask_jwt_next import __version__


def long_description():
    with open('README.md') as f:
        return f.read()


setup(
    name='flask-jwt-next',
    version=__version__.__version__,
    license='MIT',
    url='https://github.com/yannickkirschen/flask-jwt-next',
    author='Yannick Kirschen',
    author_email='github.yannickkirschen@protonmail.com',
    description='JWT token authentication for Flask apps.',
    long_description_content_type='text/markdown',
    long_description=long_description(),
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ]
)
