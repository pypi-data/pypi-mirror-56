#Created: Sun May 26 18:44:28 2019
#By: mach

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyKeller",
    version="0.0.1",
    author="Doug Keller",
    author_email="dg.kllr.jr@gmail.com",
    description="This package contains the classes and functions used for my research and engineering.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkllrjr/PyKeller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
