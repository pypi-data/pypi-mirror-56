
from setuptools import setup
import re

filepath = 'elasticConstants/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
  name = 'elasticConstants',
  version = __version__,
  author = 'Tom de Geus',
  author_email = 'tom@geus.me',
  url = 'https://github.com/tdegeus/elasticConstants',
  keywords = 'elasticity',
  description = 'Convert pair of elastic constants',
  long_description = '',
  license = 'MIT',
  packages = ['elasticConstants'],
)

