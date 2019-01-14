import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cq_jupyter",
    version = "0.9.0",
    author = "Bernhard Walter",
    author_email = "bwalter42@gmail.com",
    description = ("An extension to view X3DOM content created by CadQuery 2.x"),
    license = "Apache License 2.0",
    keywords = "x3dom cadquery visualisations",
    packages=['cq_jupyter'],
    package_data={'cq_jupyter': ['js/*', 'css/*']},
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python'",
        "Programming Language :: Python :: 3'"
    ]
)