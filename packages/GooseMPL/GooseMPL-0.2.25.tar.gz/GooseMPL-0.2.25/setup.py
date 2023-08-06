
from setuptools import setup

setup(
  name             = 'GooseMPL',
  version          = '0.2.25',
  author           = 'Tom de Geus',
  author_email     = 'tom@geus.me',
  url              = 'https://github.com/tdegeus/GooseMPL',
  keywords         = 'matplotlib, style',
  description      = 'Style and extension functions for matplotlib',
  long_description = 'Style and extension functions for matplotlib',
  license          = 'MIT',
  install_requires = ['matplotlib>=2.0.0', 'numpy>=1.0.0'],
  packages         = ['GooseMPL'],
)
