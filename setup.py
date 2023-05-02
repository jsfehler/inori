import os

from setuptools import find_packages, setup


def read(filename: str):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


def get_version_data() -> dict:
    """Read the project's version file as text."""
    data = {}

    path = os.path.join(os.path.dirname(__file__), 'inori', 'version.py')

    with open(path) as fp:
        exec(fp.read(), data)

    return data


version_data = get_version_data()


setup(
    name="inori",
    version=version_data['__version__'],
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
