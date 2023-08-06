import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="claraw10", 
    version="0.0.1",
    author="Clara",
    author_email="clara@example.com",
    description="A plotting and clustering package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claradab/claraw10",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

