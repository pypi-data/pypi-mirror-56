# -*- coding: utf-8 -*-
# python setup.py sdist bdist_wheel upload
import os

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

import setuptools

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio_aligner",
    version="1.0.1",
    author="longmao",
    author_email="sharpcx@live.com",
    description="",
    long_description_content_type="text/markdown",
    url="",
    packages=["tf_audio_manager"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=load_requirements(os.path.join(dir_path, 'requirements.txt'))
)
