#!/usr/bin/env python

from setuptools import setup

setup(name='traceanalyzer',
      version='1.0.0',
      py_modules=['traceanalyzer'],
      author='Stany Mwamba Bakajika',
      author_email='mwambastany@gmail.com',
      url='https://github.com/StanyMwamba/traceanalyzer',
      download_url='http://packages.python.org/tracenalyzer',
      license='http://opensource.org/licenses/MIT',
      description='This library  provides analyzing and plotting functions of ns2 trace file in Python.',
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
