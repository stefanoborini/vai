#!/usr/bin/env python3.4
import sys

if '3.4' not in sys.version.split()[0]:
    print("Needs python 3.4")
    sys.exit(0)

import os
import codecs
import re
from setuptools import setup, find_packages



base_dir = os.path.abspath(os.path.dirname(__file__))
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(base_dir, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Get the long description from the relevant file
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "vai",
    version = find_version("vai", "__init__.py"),
    author = "Stefano Borini",
    author_email = "stefano.borini@gmail.com",
    description = "VAI is a console-based IDE similar to VIM",
    license = "BSD",
    keywords = "editor",
    url="https://github.com/stefanoborini/vai",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Editors",
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite = 'nose.collector',
    install_requires = ['pygments==2.0.1', "pylint==1.3.0", 'pyflakes==0.8.1', 'yapsy==1.10.423'],
    entry_points={
        'console_scripts': [
            'vai_exec=vai:main',
        ],
    },
    scripts=['bin/vai'],
    zip_safe=False,
)

