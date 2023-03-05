from os.path import isfile
from setuptools import setup, find_packages

setup(
    name = "uno_synth",
    version = "0.2.0",
    author = "Simon Wood",
    author_email = "simon@mungewell.org",
    description = "Library for working with Uno Synth config files",
    license = "GPLv3",
    keywords = "Uno synth",
    url = "https://github.com/mungewell/uno-synth-utils",
    py_modules=["uno_synth"],
    long_description=open("README.rst").read() if isfile("README.rst") else "",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
)
