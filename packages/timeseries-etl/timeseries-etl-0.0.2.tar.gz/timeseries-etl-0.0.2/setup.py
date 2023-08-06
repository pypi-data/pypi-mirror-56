import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="timeseries-etl",
    version="0.0.2",
    author="Alvaro Brandon",
    author_email="alvaro.brandon@kapsch.net",
    description="A series of utils to extract timeseries data from a DB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gde.kapschtraffic.com/brandon/py_analytics_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)