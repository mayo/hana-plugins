#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-excerpts',
    version='0.0.1',

    description='Excerpts plugin for Hana static site generator',

    install_requires=[
        'beautifulsoup4>=4.6.0',
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

    packages=['hana_plugins'],

    entry_points={
        'hana_plugins': [
            'exceprts = hana_plugins.exceprts:exceprts',
        ]
    }
)

