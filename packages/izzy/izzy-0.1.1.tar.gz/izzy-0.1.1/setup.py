"""
setup.py
--------

The purpose of this script is to install izzy
"""

from setuptools import setup
import yaml


# Read version
with open('version.yml', 'r') as f:
    version = yaml.safe_load(f.read())

# Setup
setup(
    name='izzy',
    version=str(version['major']) + '.' + str(version['minor']) + '.' + str(version['build']),
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
    install_requires=[
        'google-api-python-client',
        'google-cloud-bigquery',
        'google_auth',
        'google_auth_oauthlib',
        'matplotlib',
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
        'wheel',
    ],
    zip_safe=True
)
