from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join('InSpice', '__init__.py'), 'r') as f:
    init_content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_content, re.M)
    version = version_match.group(1) if version_match else '0.1.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="InSpice",
    version=version,
    description="Python interface to Ngspice and Xyce circuit simulators (forked from PySpice)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Innovoltive",
    author_email="info@innovoltive.com",
    url="https://github.com/Innovoltive/InSpice",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "PyYAML",
        "cffi>=1.0.0",
        "diskcache",
        "h5py",
    ],
    extras_require={
        "dev": ["pytest", "twine", "build"],
    },
    entry_points={
        "console_scripts": [
            "inspice-post-installation=InSpice.Scripts.InSpice_post_installation:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires='>=3.8',
)