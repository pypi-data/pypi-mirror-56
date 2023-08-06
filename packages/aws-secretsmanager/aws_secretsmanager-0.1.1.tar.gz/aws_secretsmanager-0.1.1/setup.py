#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='aws_secretsmanager',
    version='0.1.1',
    packages=[ 'aws_secretsmanager' ],
    install_requires=[ 'boto3' ],
    extras_require={
        "test": [ 'pytest>=3.0']
    },
    provides=[ 'aws_secretsmanager' ],
    author='Justin Menga',
    author_email='justin.menga@gmail.com',
    url='https://github.com/mixja/aws-secretsmanager',
    description='Manager that fetches and processes updates for AWS Secrets Manager secrets',
    keywords='aws secretsmanager secrets',
    license='ISC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)