import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micpy",
    version="0.0.1",
    author="Amir Rouhollahi",
    author_email="rouhollahi@outlook.com",
    description="A python package for microscopic image analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirrouh/micpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)