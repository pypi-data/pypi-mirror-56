"""
setup.py
--------

The purpose of this script is to install izzy
"""

import numpy as np
from setuptools import setup
import yaml


# Read version
with open('version.yml', 'r') as f:
    version_data = yaml.safe_load(f.read())

# Convert the version_data to a string
version = str(version_data['major']) + '.' + str(version_data['minor'])
if 'build' in version_data:
    version += '.' + str(version_data['build'] - version_data['build_offset'])

# Read in requirements.txt
requirements = np.loadtxt('requirements.txt', dtype='str').tolist()

# Setup
setup(
    name='izzy',
    version=version,
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='A toolkit for executing and analyzing machine learning classification',
    long_description='A toolkit for executing and analyzing machine learning classification',
    long_description_content_type='text/x-rst',
    url="https://www.lockhartlab.org",
    packages=[
        'izzy',
        'izzy.datasets',
        'izzy.eda',
        'izzy.features',
        'izzy.io',
        'izzy.misc',
        'izzy.classification',
        'izzy.regression',
        'izzy.viz',
    ],
    install_requires=requirements,
    zip_safe=True
)
