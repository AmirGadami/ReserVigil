from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqirements = f.read().splitlines()

setup(

    name='MLOps_Project',
    version = '1.0.0',
    packages= find_packages(),
    install_requires=reqirements

)

