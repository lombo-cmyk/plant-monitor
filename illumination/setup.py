from setuptools import setup, find_packages


setup(
    name='illumination',
    version='0.0.1',
    description='Diodes illumination',
    author='lombo-cmyk',
    url='https://github.com/lombo-cmyk/plants-grow',
    packages=find_packages(exclude=('tests', 'docs'))
)