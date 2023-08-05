from setuptools import setup, find_packages

setup(
    name = 'sas-sample-app',
    version = '1.1.5',
    description = 'step 1 Tutorial',
    author = 'Viswanathan Muthiah',
    author_email = 'viswanathan.m1@tcs.com',
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['azure-storage-blob'],
    setup_requires = ['wheel']
)