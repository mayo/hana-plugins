#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-webmentions',
    version='0.0.1',

    description='Front matter plugin for Hana static site generator',

    install_requires=[
        'ronkyuu>=0.6.0',
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
            'find_webmentions = hana_plugins.webmentions.FindWebmentions',
            'send_webmentions = hana_plugins.webmentions.SendWebmentions',
        ]
    }
)

