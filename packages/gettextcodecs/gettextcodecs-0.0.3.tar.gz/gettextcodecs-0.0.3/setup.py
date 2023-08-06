#!/usr/bin/env python3
from setuptools import setup
import os
import sys

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='gettextcodecs',
      version='0.0.3',
      description='Get python\'s text codecs',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://gitlab.com/xoristzatziki/gettextcodecs',
      author='Ηλίας Ηλιάδης',
      author_email='iliadis@kekbay.gr',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      license='GPLv3',
      packages=['gettextcodecs'],
      include_package_data=True,
      zip_safe=False)
