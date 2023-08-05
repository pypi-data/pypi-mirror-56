import distutils

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    distutils.dir_util.remove_tree

setuptools.setup(
    name="pydspdm",
    version="0.0.10",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)