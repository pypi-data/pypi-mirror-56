import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="My-Pack-Zach-Zemo", # Replace with your own username
    version="0.0.1",
    author="Zach Zemokhol",
    author_email="zachzemokhol@gmail.com",
    description="Exploring the scikitlearn wine dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZachZemo/final-pack.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
