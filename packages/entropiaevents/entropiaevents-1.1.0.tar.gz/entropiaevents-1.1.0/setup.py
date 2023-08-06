# coding=utf-8

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='entropiaevents',
    version='1.1.0',
    author='Christian Lölkes',
    author_email='christian.loelkes@gmail.com',
    description='Fetchs events from entropia.de',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/entropia/py-entropiaevents.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
    install_requires=[
        'obelixtools'
    ],
)
