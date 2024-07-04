"""setup.py file for packaging"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SciContext",
    version="0.2",
    author="Stuart Chalk",
    author_email="schalk@unf.edu",
    description="An Django webapp for management and storage of JSON-LD context files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chalklab/SciContext",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
