# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

here = os.path.dirname(__file__)

with open(os.path.join(here, "requirements.txt"), "r") as f:
    requirements = f.read().split("\n")

setup(name='templot',
      version='0.4',
      description="Python package for visualizing time evolution.",
      long_description="This package offers various functions for visually exploring data variation in time",
      author='Khalil Kacem',
      author_email='khail@kacem.xyz',
      url='https://github.com/khllkcm/templot',
      packages=find_packages(),
      requires=requirements,
      include_package_data=True)
