from setuptools import setup, find_packages
from os import path
from io import open
import epicenter

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='epicenter',
      version=epicenter.__version__,
      packages=['epicenter'],
      url='http://www.forio.com/epicenter',
      description=('Python Package for interacting with the Forio '
                   'Epicenter Platform'),
      long_description='Python Package for interacting with the Forio Epicenter Platform',
      author='Forio',
      author_email='tech@forio.com',
      keywords=['Forio', 'Epicenter'],
      license='Apache License 2.0'
      )
