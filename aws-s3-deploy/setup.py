#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

setup(name='hana-plugin-aws-s3-deploy',
    version='0.0.1',

    description='AWS S3 Deployment plugin for Hana static site generator',

    install_requires=[
        'boto3>=1.5.8',
        'python-magic>=0.4.15',
    ],

    author='Mayo Jordanov',
    author_email='mayo@oyam.ca',

    url='https://github.com/mayo/hana-plugins',

    license='MIT',

    classifiers=[
        'Programming Language :: Python',
    ],

    keywords='hana front matter metadata',

    packages=['hana.plugins'],

    entry_points={
        'hana.plugins': [
            'aws_s3_deploy = hana.plugins.s3_deploy:AWSS3Deploy',
        ],
        'hana.commands': [
            'aws_s3_deploy = hana.plugins.aws_s3_deploy:AWSS3Commands',
        ]
    }
)

