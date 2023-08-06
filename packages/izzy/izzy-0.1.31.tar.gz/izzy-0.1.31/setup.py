"""
setup.py
--------

The purpose of this script is to install izzy
"""

from setuptools import setup
import yaml


# Read version
with open('version.yml', 'r') as f:
    version_data = yaml.safe_load(f.read())

# Convert the version_data to a string
keys = ['major', 'minor']
if 'build' in version_data:
    keys.append('build')
version = '.'.join([str(version_data[key]) for key in keys])

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
    install_requires=[
        'google-api-python-client',
        'google-cloud-bigquery',
        'google_auth',
        'google_auth_oauthlib',
        'matplotlib',
        'numpy',
        'pandas',
        'pyyaml',
        'scikit-learn',
        'scipy',
        'wheel',
    ],
    zip_safe=True
)
