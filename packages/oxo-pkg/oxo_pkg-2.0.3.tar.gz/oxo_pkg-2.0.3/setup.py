import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oxo_pkg",
    version="2.0.3",
    author="Adam Harrison",
    author_email="author@example.com",
    description="naughts and crosses game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tbd",
    scripts=["bin/oxo"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
