#!/usr/local/bin python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="gitProjTool",
    version="0.0.1",
    author="Onion-Shen",
    author_email="18513385631@163.com",
    url="https://github.com/Onion-Shen/GitProjectTool",
    description="a tool that analyse project on git",
    packages=["GitProjectTool"],
    install_requires=["prettytable"],
    entry_points={
        'console_scripts': [
            "GitProjectTool=GitProjectTool:run"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
    ]
)
