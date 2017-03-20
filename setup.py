#!/usr/bin/env python

from setuptools import setup


__pkg_name__ = 'lambdax'
__author__ = "Hugues Lerebours"

VERSION = '0.0.1'
DESCRIPTION = "Write lambda expressions in a simpler way"

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


if __name__ == '__main__':
    setup(
        name=__pkg_name__,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        classifiers=CLASSIFIERS,
        author=__author__,
        author_email="hugues@lereboursp.net",
        url="https://github.com/hlerebours/lambda-calculus",
        license="MIT License",
        packages=['lambdax', 'lambdax.test'],
        setup_requires=['pytest-runner>=2.11', 'pylama_pylint>=3.0'],
        tests_require=['pytest>=3.0', 'pytest-cov>=2.4', 'pylint>=1.6', 'pylama>=7.3'],
        platforms=['any']
    )
