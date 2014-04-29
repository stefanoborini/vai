import os
from setuptools import setup

setup(
    name = "vix",
    version = "1.0",
    author = "Stefano Borini",
    author_email = "stefano.borini@gmail.com",
    description = ("VIX is a console-based IDE similar to VIM"),
    license = "BSD",
    keywords = "editor",
    url = "",
    packages=['vix', 'tests'],
    long_description="VIX is a console-based IDE similar to VIM",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    test_suite = 'nose.collector'
)
