import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apextras",
    version="0.9.1",
    author="David Zerrenner",
    author_email="dazer017@gmail.com",
    description="Some helpers for python's argparse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypyr-scheduler/python-argparse-extras",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
