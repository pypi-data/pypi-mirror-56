import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="raingbow",
    version="1.1",
    author="Max Saganyuk",
    author_email="makssagan1@mail.ru",
    description="Module for rough translation of visible light wavelength values to RGB-color values",
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    python_requires=">=3.6"
)
