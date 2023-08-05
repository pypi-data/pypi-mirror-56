#!/usr/bin/env python

from setuptools import setup
#reading the contents of README.md file
from os import path
this_directory=path.abspath(path.dirname(__file__))
with open(path.join(this_directory,'README.md'),encoding='utf-8') as f:
    long_description=f.read()
setup(name='traceanalyzer',
      version='1.0.1',
      py_modules=['traceanalyzer'],
      author='Stany Mwamba Bakajika',
      author_email='mwambastany@gmail.com',
      url='https://github.com/StanyMwamba/traceanalyzer',
      download_url='http://packages.python.org/tracenalyzer',
      license='http://opensource.org/licenses/MIT',
      description='This library  provides analyzing and plotting functions for ns2 trace file in Python.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='NS2 trace file',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Text Processing :: General',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Education',
      ],
      install_requires=['awk>=1.2.1','matplotlib>=3.1.1'],
      python_requires='>=3.6',
      platforms='ALL',
      )
