import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = read("requirements.txt").split()

setuptools.setup(
    name="simplesearch",
    version="0.0.1",
    author="Ayoub Benaissa",
    author_email="ayouben9@gmail.com",
    description="A library for doing search on different kind of files",
    license="Apache License 2.0",
    keywords="search nlp index",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/youben11/simplesearch",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
    )
