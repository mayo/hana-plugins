#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-metadata',
    version='0.0.1',

    description='Metadata plugin for Hana static site generator',

    install_requires=[
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana metadata',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'metadata = hana.plugins.metadata:metadata',
        ]
    }
)

