import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mod-tbl-linebuilder",
    version="0.0.4",
    description="library for building line level components of a table - intended to be used as a sub-component of a full featured table constructor",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TravisLazar/travs-table-linebuilder",
    author="Travis Lazar",
    author_email="travis.lazar@gmail.com",
    license="GPLv3",
    install_requires=[
        'utflib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=("tests",)),
)