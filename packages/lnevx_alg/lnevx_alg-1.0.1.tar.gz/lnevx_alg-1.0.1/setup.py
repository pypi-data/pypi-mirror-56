from setuptools import setup, find_packages

import lnevx_alg

setup(
    name='lnevx_alg',
    version=lnevx_alg.__version__,
    packages=find_packages(),
    long_description=open('README.txt').read(),
    test_suite='tests',
)
