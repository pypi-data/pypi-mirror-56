import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parkour",
    version="0.0.2",
    author="Pat Carolan",
    author_email="patrick.carolan@gmail.com",
    description="Data utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcarolan/parkour",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)