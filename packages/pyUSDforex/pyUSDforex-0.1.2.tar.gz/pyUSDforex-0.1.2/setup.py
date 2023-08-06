import pathlib2
import setuptools

# The directory containing this file
HERE = pathlib2.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="pyUSDforex",
    version="0.1.2",
    author="Lawrence Stewart",
    author_email="lawrence@lawrencestewart.ca",
    description="Converts foreign fiat currencies to USD by getting and caching hourly exchanges rates from openexchangerates.org",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/getorca/pyUSDforex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
