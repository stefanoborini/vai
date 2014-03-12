import os
from setuptools import setup

setup(
    name = "vide",
    version = "1.0",
    author = "Stefano BoriniCarter",
    author_email = "stefano.borini@ferrara.linux.it",
    description = ("VIDE a Vim IDE"),
    license = "BSD",
    keywords = "editor",
    url = "",
    packages=['vide', 'tests'],
    long_description="Whatever",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
