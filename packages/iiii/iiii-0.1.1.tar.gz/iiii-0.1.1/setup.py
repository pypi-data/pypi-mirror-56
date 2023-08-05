import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iiii", # Replace with your own username
    version="0.1.1",
    author="David M. Golembiowski",
    author_email="dmgolembiowski@gmail.com",
    description="iiii [Four Eyes], a search engine that helps you look wider and deeper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmgolembiowski/iiii",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
