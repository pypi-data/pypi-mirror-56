"""
setup.py
--------

The purpose of this script is to install izzy
"""

from setuptools import setup
# from numpy.distutils.core import setup

setup(
    name='izzy',
    version='0.1',
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
