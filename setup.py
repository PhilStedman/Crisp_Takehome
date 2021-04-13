from setuptools import find_packages, setup

with open("README.md") as fp:
   long_description = fp.read()

setup(
    name='philcsv',
    python_requires='>=3.8.5',
    packages=find_packages(include=['philcsv']),
    version='0.1.0',
    description='Crisp Take Home Library',
    long_description=long_description,
    author='Phil Stedman',
    license='GPL',
    install_requires=['pandas'],
)
