import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("synbiopython/version.py").read())  # loads __version__

setuptools.setup(
    name="synbiopython",
    version=__version__,
    author="Global Biofundries Alliance",
    author_email="author@example.com",
    description="Python tools for Synthetic Biology.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Global-Biofoundries-Alliance/SynBioPython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)