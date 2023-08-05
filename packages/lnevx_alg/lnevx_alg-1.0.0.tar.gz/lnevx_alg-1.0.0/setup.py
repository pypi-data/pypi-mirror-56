from setuptools import setup, find_packages
from os.path import join, dirname

import lnevx_alg

setup(
    name='lnevx_alg',
    version=lnevx_alg.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    test_suite='tests',
)
