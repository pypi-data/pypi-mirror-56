import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helloworld-ajilraju", # Replace with your own username
    version="0.0.3",
    author="Ajil Raju",
    author_email="ajilraju01@gmail.com",
    description="A package to print hello world",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajilraju/pypa-helloworld",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
