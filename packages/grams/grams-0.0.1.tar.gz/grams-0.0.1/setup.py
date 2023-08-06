import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grams",
    version="0.0.1",
    author="Jonasz Rice",
    author_email="jonaszakr@gmail.com",
    description="A package for dealing with histograms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/escofresco/makeschool_fsp2_realtweets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy==1.17.3",
        "dit==1.2.3",
    ])
