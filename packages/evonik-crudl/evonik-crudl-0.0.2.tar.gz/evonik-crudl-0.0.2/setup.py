import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evonik-crudl",
    version="0.0.2",
    author="Benjamin Schiller",
    author_email="benjamin.schiller@evonik.com",
    description="CRUDL wrappers for databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://evodl.visualstudio.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "mysql-connector"
    ],
)
