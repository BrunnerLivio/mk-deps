# -*- coding: utf-8 -*-

"""
    Setup mk-deps
"""

import ast
import re
from setuptools import setup, find_packages

def get_version():
    """Gets the current version"""
    _version_re = re.compile(r"__VERSION__\s+=\s+(.*)")
    with open("mkdeb/__init__.py", "rb") as init_file:
        version = str(ast.literal_eval(_version_re.search(
            init_file.read().decode("utf-8")).group(1)))
    return version

setup(
    name="mk-deps",
    version=get_version(),
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mk-deps = mkdeb.cli:main"
        ]
    }
)
