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


github_url = 'https://github.com/escodebar/django-rest-framework-rules'

setup(
    name='django-rest-framework-rules',
    description='Django REST framework integration for django-rules',
    version=get_version(VERSION),
    long_description=long_description,
    url=github_url,
    download_url=('{github_url}/archive/v{version}.tar.gz'
                  .format(github_url=github_url,
                          version=get_version(VERSION))),
    author='Pablo Escodebar',
    author_email='escodebar@gmail.com',
    maintainer='Pablo Escodebar',
    maintainer_email='escodebar@gmail.com',
    license='MIT',
    packages=['rest_framework_rules'],
    install_requires=['django', 'rules'],
    python_requires='>=3.5.*, <4',
    py_modules=['six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
