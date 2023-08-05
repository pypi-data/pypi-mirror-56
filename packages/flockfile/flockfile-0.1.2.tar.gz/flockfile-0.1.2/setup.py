#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.2"

def readme():
    """ print long description """
    with open('README.md') as f:
        long_descrip = f.read()
    return long_descrip

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CI_COMMIT_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="flockfile",
    version=VERSION,
    description="A simple lock file class based on file locking.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rveach/flockfile",
    project_urls={
        'Source': "https://gitlab.com/rveach/flockfile",
        'Tracker': 'https://gitlab.com/rveach/flockfile/issues',
    },
    author="Ryan Veach",
    author_email="rveach@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',    ],
    keywords=['Lock', 'Flock'],
    packages=['flockfile'],
    install_requires=[
    ],
    python_requires='>=2.7',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)