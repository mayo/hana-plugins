#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-cloudflare',
    version='0.0.1',

    description='CloudFlare tools',

    install_requires=[
        'cloudflare>=2.1.0',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana cloudflare cdn',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'cloudflare_purge_cache = hana.plugins.cloudflare:purge_cache',
        ]
    }
)

