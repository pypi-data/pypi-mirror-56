# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('Readme.md') as f:
        readme = f.read()

with open('LICENSE') as f:
    license = f.read()
    
setup(
    name='fBms',
    version='0.1.2',
    description='Fractal Brownian motion',
    long_description=readme,
    classifiers=[
        'Development status :: 1 - Alpha',
        'License :: CC-By-SA2.0',
        'Programming Language :: Python',
        'Topic :: Gaussian Random Field'
    ],
    author='Antoine Marchal',
    author_email='amarchal@cita.utoronto.ca',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'numpy',
    ],
    include_package_data=True
)
