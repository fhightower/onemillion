#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Requests',
    'docopt>=0.6',
]

test_requirements = [
    'Requests'
]

setup(
    name='onemillion',
    version='1.0.0',
    description="Determine if a domain is in the Alexa or Cisco top one million domain list.",
    long_description=readme + '\n\n' + history,
    author="Floyd Hightower",
    author_email='',
    entry_points={
       'console_scripts': [
           'onemillion=onemillion.cli:main'
       ]
    },
    url='https://github.com/fhightower/onemillion',
    packages=[
        'onemillion',
    ],
    package_dir={'onemillion':
                 'onemillion'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='onemillion',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
