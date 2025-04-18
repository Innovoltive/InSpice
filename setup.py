from setuptools import setup, find_packages

setup(
    name="InSpice",
    version="0.1.0",
    description="Python interface to Ngspice and Xyce circuit simulators (forked from PySpice)",
    author="Innovoltive",
    author_email="info@innovoltive.com",
    url="https://github.com/Innovoltive/InSpice",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)