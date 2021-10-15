import os

from setuptools import find_packages, setup


def read(filename:str):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


setup(
    name="inori",
    version="0.0.6",
    description="The Universal API Client Constructor.",
    long_description=read('README.rst'),
    author="Joshua Fehler",
    license="GPLv3",
    url="https://github.com/jsfehler/inori",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'shibari>=0.0.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
