# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.
# pylint: skip-file
from setuptools import setup
import os

version = '2.3.0'

long_description = open('README.md').read()

test_requirements = [
    'pytest'
]

setup(
    name='s11-classifier',
    version=version,
    description="Classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rens Masselink",
    author_email='rens.masselink@satelligence.com',
    url='https://gitlab.com/satelligence/classifier',
    packages=[
        'classifier',
    ],
    package_dir={'classifier':
                 'classifier'},
    include_package_data=True,
    license="Apache-2.0",
    zip_safe=False,
    python_requires='>=3.5'
)
