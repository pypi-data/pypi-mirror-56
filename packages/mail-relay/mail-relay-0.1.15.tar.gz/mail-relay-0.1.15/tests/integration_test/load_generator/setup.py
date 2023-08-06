# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='load_generator',
    version='0.0.1',
    author='Saman Tehrani',
    author_email='samanrtehrani@gmail.com',
    entry_points={
      'console_scripts': [
        'generate = load_generator:generate'
      ]
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=2.7'
)
