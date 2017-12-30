#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-collections',
    version='0.0.1',

    description='Collections plugin for Hana static site generator',

    install_requires=[
        'pathspec>=0.5.2',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana front matter metadata',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'collections = hana.plugins.collections.Collections',
        ]
    }
)

