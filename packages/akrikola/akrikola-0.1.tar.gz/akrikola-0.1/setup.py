from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='akrikola',
    version='0.1',
    description='A light-weight NLP library for Finnish language',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    url='http://github.com/tjkemp/akrikola',
    author='Tjkemp',
    author_email='tero.kemppi@gmail.com',
    license='GNU LGPLv3',
    packages=[],
    zip_safe=False
    )
