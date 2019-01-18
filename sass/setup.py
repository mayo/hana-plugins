#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-sass',
    version='0.0.1',

    description='SASS plugin for Hana static site generator',

    install_requires=[
        'libsass>=0.17.0',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana sass metadata',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'sass = hana.plugins.sass.Sass',
        ]
    }
)

