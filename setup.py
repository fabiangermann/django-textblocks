#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-textblocks',
    version='0.8.3',
    description='Simple app for managing small blocks of text/html.',
    long_description=read('README.rst'),
    author='Fabian Germann',
    author_email='fg@feinheit.ch',
    url='http://github.com/fabiangermann/django-textblocks/',
    packages=find_packages(
        exclude=['tests'],
    ),
    include_package_data=True,
    install_requires=[
        # 'Django>=1.7.0',
        'django-modeltranslation>=0.8',
        'six',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
