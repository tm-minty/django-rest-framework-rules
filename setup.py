#!/usr/bin/env python
from os.path import dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from rest_framework_rules import VERSION


def get_version(version):
    return '.'.join(map(str, version))


with open(join(dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


setup(
    name='rest_framework_rules',
    description='Django REST framework integration for rules',
    version=get_version(VERSION),
    long_description=long_description,

    url='https://github.com/escodebar/django-rest-framework-rules',
    download_url='https://github.com/escodebar/django-rest-framework-rules/archive/v0.1.tar.gz',
    author='Pablo Escodebar',
    author_email='escodebar@gmail.com',
    maintainer='Pablo Escodebar',
    maintainer_email='escodebar@gmail.com',
    license='MIT',

    packages=[
        'rest_framework_rules',
    ],

    install_requires=[
        'Django>=1.9',
        'djangorestframework>=3.6',
        'rules>=1.2.1',
        'six',
    ],
    extras_require={
        'test': [
            'nose',
            'coverage',
            'Django>=1.5',
            'djangorestframework',
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
