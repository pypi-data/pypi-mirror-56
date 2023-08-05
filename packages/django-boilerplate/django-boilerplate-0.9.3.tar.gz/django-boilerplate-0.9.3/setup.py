#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import boilerplate

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = boilerplate.__version__

if sys.argv[-1] == 'publish':
    os.system('cd docs && make html')
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

if sys.argv[-1] == 'test':
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system('python manage.py test')
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='django-boilerplate',
    version=version,
    description="""What Django is missing""",
    long_description=readme + '\n\n' + history,
    author='Irving Kcam',
    author_email='me@ikcam.com',
    url='https://github.com/cubope/django-boilerplate',
    packages=[
        'boilerplate',
    ],
    include_package_data=True,
    install_requires=['Pillow', 'six'],
    license="Apache License 2.0",
    zip_safe=False,
    keywords='django-boilerplate',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
