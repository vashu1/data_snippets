import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "count_areas",
    version = "0.0.1",
    author = "Ivan Bondar",
    author_email = "ivan.e.bondar@gmail.com",
    description = ("Count number of colored areas in an bitmap."),
    license = "BSD",
    packages=['images'],
    scripts=['count-areas'],
    install_requires=required,
)
