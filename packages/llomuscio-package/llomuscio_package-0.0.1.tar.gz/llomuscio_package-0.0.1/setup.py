import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llomuscio_package",
    version="0.0.1",
    author="Lucas L",
    author_email="lucas@example.com",
    description="My example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bobbycookie/Package_Lucas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)