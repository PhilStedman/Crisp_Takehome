from setuptools import find_packages, setup

setup(
    name='philcsv',
    packages=find_packages(include=['philcsv']),
    version='0.1.0',
    description='Crisp Take Home Library',
    author='Phil Stedman',
    license='GPL',
    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
