from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='generatecpcryptogram',
    version='1.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Natalia Deryuzhova',
    author_email='derujovanv1993@gmail.com',
    url='https://github.com/NataliaDeryuzhova/generate_cloud_payments_cryptogram',
    install_requires=[
            'pycryptodome==3.9.4'
        ],
)