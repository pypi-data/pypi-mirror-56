#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='cquai-ml',
    version='1.0.5',
    description=(
        'Implement machine learning algorithms with python without sklearn.'
    ),
    long_description=open('README.rst').read(),
    author='CQU-AI',
    author_email='peter@mail.loopy.tech',
    maintainer='loopyme',
    maintainer_email='peter@mail.loopy.tech',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/CQU-AI/ML-Algorithm',
    install_requires=[
        'tabulate>=0.8.5',
        'tqdm>=4.38.0',
        'requests>=2.22.0',
        'numpy>=1.17.4',
        'pandas>=0.25.3',
        'sklearn>=0.0'
    ]
)
