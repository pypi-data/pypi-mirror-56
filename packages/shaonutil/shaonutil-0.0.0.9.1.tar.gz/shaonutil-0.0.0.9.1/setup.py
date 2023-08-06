#from distutils.core import setup
from setuptools import setup
from shaonutil.file import read_configuration_ini
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

configs = read_configuration_ini('setup_config.ini')

setup(
  name = configs['SETUP']['name'],
  packages = configs['SETUP']['packages'].split(','),
  version = configs['SETUP']['version'],
  long_description=long_description,
  long_description_content_type=configs['SETUP']['long_description_content_type'],
  author = configs['SETUP']['author'],
  author_email = configs['SETUP']['author_email'],
  url = configs['SETUP']['url'],
  download_url = configs['SETUP']['download_url'],
  keywords = configs['SETUP']['keywords'].split(','),
  classifiers = [],
)