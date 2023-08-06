import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rinjani",
    version="1.0.3",
    author="Connor Beard",
    author_email="Connor-Beard@hotmail.com",
    description="A Web Scraping Package for ML/Sentiment Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/legacy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
