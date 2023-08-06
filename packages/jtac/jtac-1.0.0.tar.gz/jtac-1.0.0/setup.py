#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

with open('requirements_test.txt') as f:
    req_test = f.read().splitlines()

with open('requirements_dev.txt') as f:
    req_devs = f.read().splitlines()


requirements = reqs

setup_requirements = req_devs

test_requirements = req_test

setup(
    author="Andrés Franco Riquelme Sandoval",
    author_email='andresfranco.rs@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Start, stop and restart your arma servers just with cli",
    entry_points={
        'console_scripts': [
            'jtac=jtac.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='jtac',
    name='jtac',
    packages=find_packages(include=['jtac']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/corp-0/jtac',
    version='1.0.0',
    zip_safe=False,
)
