#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
from clarity import __version__

setup(
    name="clarity",
    packages=["clarity"],
    version=__version__,
    license="MIT",
    description="A colored logger for python",
    author="singhsays",
    author_email="singhsays@gmail.com",
    url="https://github.com/rockstardevs/clarity-py",
    download_url="https://github.com/rockstardevs/clarity-py/archive/v0.1.0.tar.gz",
    keywords=["logging", "absl", "log",],
    install_requires=["absl-py", "colored",],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: Other",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=open("README.md").read(),
)
