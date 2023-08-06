# -* coding: utf-8 *-
from setuptools import setup, find_packages
from os import path
from io import open

import dockager


HERE = path.abspath(path.dirname(__file__))


with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='dockager',
    version=dockager.__version__,
    description='Dockager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgarana/dockager',
    author='David Garaña',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='docker-compose packager',
    entry_points = {
        'console_scripts': ['dockager=dockager.dockager_cli:main'],
    },
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[]
)
