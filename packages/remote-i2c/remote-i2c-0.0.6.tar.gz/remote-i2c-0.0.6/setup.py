import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remote-i2c",
    version="0.0.6",
    author="Daniel 'Vector' Kerr",
    author_email="vector@vector.id.au",
    description="A client and server for I2C control over TCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vectoridau/remote-i2c",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
        "Topic :: System :: Networking",
        "Topic :: Utilities"
    ],
    python_requires='>=3',
)
