#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-pretty-url',
    version='0.0.1',

    description='Pretty URL plugin for Hana static site generator',

    install_requires=[
        'hana',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana',

    packages=['hana_plugins'],

    entry_points={
        'hana_plugins': [
            'pretty_url = hana_plugins.pretty_url.PrettyUrl',
        ]
    }
)

