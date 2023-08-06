from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='onnds',
    version='0.0.13',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='http://oznetnerd.com',
    install_requires=[
        'deep-security-api>=12.0.327',
        'onnlogger==0.0.3',
        'requests>=2.22.0',
    ],
    license='',
    author='Will Robinson',
    author_email='will@oznetnerd.com',
    description='Convenience module for interacting with Trend Micro Deep Security'
)
