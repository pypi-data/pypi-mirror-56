#!/usr/bin/env python

from setuptools import setup
from glob import glob

NAME = "elicit"

with open('README.md') as fo:
    LONG_DESCRIPTION = fo.read()


setup(
    name=NAME,
    packages=["elicit", "elicit.present"],
    install_requires=[],
    scripts=glob("bin/*"),
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    test_suite="tests",
    tests_require=["pytest"],
    package_data={"elicit.present": ["data/*.png"]},

    description="Library for making command-style user interfaces.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license="Apache 2.0",
    author="Keith Dart",
    author_email="keith@dartworks.biz",
    url="https://github.com/kdart/elicit",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Debuggers",
    ],
)

# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
