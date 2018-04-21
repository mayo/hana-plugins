#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-micro_blog',
    version='0.0.1',

    description='Micro.blog helpers',

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

    keywords='hana micro.blog',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'micro_blog_ping = hana.plugins.micro_blog:ping',
        ]
    }
)

