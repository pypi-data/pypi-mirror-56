import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="hipster",
    version="3.0.3",
    description="A thread safe implementation of the MinHeap and MaxHeap",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/soumasish/hipster",
    author="Soumasish Goswami",
    author_email="soumasish@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['readerwriterlock', ],
)
