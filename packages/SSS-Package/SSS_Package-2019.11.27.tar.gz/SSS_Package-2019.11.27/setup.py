import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SSS_Package",
    version="2019.11.27",
    author="Sergii Serednii",
    author_email="sseredniy@gmail.com",
    description="Set of useful functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SergiiSerednii",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)