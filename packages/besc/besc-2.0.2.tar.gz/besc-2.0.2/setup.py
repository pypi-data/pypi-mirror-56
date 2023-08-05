from setuptools import setup, find_packages

setup(
    name='besc',
    version='2.0.2',
    packages=find_packages(),
    license='MIT License',
    description='Send data to the ESS API BESC',
    download_url='https://github.com/rock98rock/BESC-API/archive/1.0.tar.gz',
    install_requires=['query_string', 'requests'],
    author='Clive Lim'
)
