#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-jinja',
    version='0.0.1',

    description='Jinja templating for Hana static site generator',

    install_requires=[
        'JInja2>=2.9.6',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana static site template',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'jinja_templates = hana.plugins.jinja.JinjaTemplates',
        ]
    }
)

