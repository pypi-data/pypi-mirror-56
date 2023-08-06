import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gersyll",
    version="1.3",
    author="gakonorde",
    author_email="gabrielko@yandex.ru",
    description="This module counts the number of words of different syllable lenght for all texts in a directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gakonorde/gersyll",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
