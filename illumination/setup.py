from setuptools import find_packages, setup

setup(
    name="illumination",
    version="0.0.1",
    description="Diodes illumination",
    author="lombo-cmyk",
    url="https://github.com/lombo-cmyk/plants-grow",
    packages=find_packages(exclude=("tests", "docs")),
)
