import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="random-genetic-forest",
    version="0.0a2",
    author="Timothy Bennett",
    author_email="tabdevelopment1@gmail.com",
    description="This is a machine learning package that includes a theoretical optimized variation of the random forest learning algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tab-dev/Random-Genetic-Forest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.7',
)