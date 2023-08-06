from sensational import __version__ as sensational_version
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="sensational",
    version=sensational_version,
    author="Daniel 'Vector' Kerr",
    author_email="vector@vector.id.au",
    description="A python library for interfacing with various sensors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vectoridau/sensational",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
        "Topic :: Utilities"
    ],
    python_requires='>=3',
)
