import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyPrivacy",
    version="0.0.1",
    author="Eugene Bagdasaryan",
    author_email="eugene@cs.cornell.edu",
    description="A Python framework to implement command-level privacy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ancile-project/pyprivacy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
