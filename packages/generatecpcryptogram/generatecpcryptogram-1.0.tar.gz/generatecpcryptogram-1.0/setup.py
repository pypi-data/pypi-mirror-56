from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='generatecpcryptogram',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Natalia Deryuzhova',
    author_email='derujovanv1993@gmail.com',
    install_requires=[
            'pycryptodome==3.9.4'
        ],
)