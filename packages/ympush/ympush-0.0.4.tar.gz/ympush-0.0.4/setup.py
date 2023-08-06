# -*- encoding: utf-8 -*-
"""
Time    : 2019/11/28 10:34
Author  : Ziggy
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ympush", # Replace with your own username
    version="0.0.4",
    author="ziggy",
    author_email="zeddshiw@gmail.com",
    description="ym push lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
