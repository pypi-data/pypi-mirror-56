import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypercube-client",
    version="0.0.1",
    author="HyperCube, Inc.",
    author_email="info@hypercube.ai",
    description="HyperCube client libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hypercubesystems/",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence"],
    python_requires=">=3.6"
)
