import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httpcodes",
    version="1.0.0",
    author="rickgrammer",
    author_email="rickgrammer@schwifty.tech",
    description="A very minimal http-status-message to http-status-code package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rickgrammer/httpcodes.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)