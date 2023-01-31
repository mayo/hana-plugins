#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-git',
    version='0.0.1',

    description='Git plugin for Hana static site generator',

    install_requires=[
        'gitpython>=2.1.8',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana git',

    packages=['hana_plugins'],

    entry_points={
        'hana_plugins': [
            'git = hana_plugins.git:git',
        ]
    }
)

