import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="utflib",
    version="0.0.1",
    description="Library for accessing well named UTF characters.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TravisLazar/utflib",
    author="Travis Lazar",
    author_email="travis.lazar@gmail.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=("tests",)),
)