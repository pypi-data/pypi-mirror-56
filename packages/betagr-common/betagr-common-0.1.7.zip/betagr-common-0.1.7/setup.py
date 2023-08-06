import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="betagr-common",
    version="0.1.7",
    author="BetAgr Team",
    author_email="betagr.team@gmail.com",
    description="API-Common package for betagr-project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndsoiIo/betagr-common",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
