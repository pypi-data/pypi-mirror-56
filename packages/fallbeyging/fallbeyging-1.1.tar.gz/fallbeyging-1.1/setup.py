from setuptools import setup, find_packages

setup(name='fallbeyging',
  version='1.1',
  description='',
  url='https://github.com/slowpokesheep/fallbeyging',
  author='Slowpoke',
  scripts=['bin/fallbeyging'],
  data_files = [
      ('assets',['fallbeyging/assets/processed/bin_words_no_capital_inflection.json']),
      #('target_directory_2', glob('nested_source_dir/**/*', recursive=True)),
  ],
  packages=['fallbeyging', 'fallbeyging/assets', 'fallbeyging/bin_data', 'fallbeyging/objects'],
  #packages=find_packages(),
  install_requires=[
      'pygame',
  ],
  zip_safe=False)
