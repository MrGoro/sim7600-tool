# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.MD') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read()

setup(
    name='sim-tool',
    version='1.0.0',
    description='Python package for basic communication with SIM7600E 4G and GPS module',
    long_description=readme,
    author='Philipp Schürmann',
    author_email='spam@mrgoro.de',
    url='https://github.com/MrGoro/sim7600-tool',
    license=license,
    packages=find_packages(exclude=('debian')),
    install_requires=required
)
