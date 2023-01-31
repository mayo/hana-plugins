#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-frontmatter',
    version='0.0.1',

    description='Front matter plugin for Hana static site generator',

    install_requires=[
        'python-frontmatter>=0.4.2',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana static site front matter metadata',

    packages=['hana_plugins'],

    entry_points={
        'hana_plugins': [
            'frontmatter = hana_plugins.frontmatter:frontmatter',
        ]
    }
)

