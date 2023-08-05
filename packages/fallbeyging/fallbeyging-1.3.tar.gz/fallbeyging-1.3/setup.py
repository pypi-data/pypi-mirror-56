from setuptools import setup, find_packages

setup(name='fallbeyging',
  version='1.3',
  description='',
  url='https://github.com/slowpokesheep/fallbeyging',
  author='Slowpoke',
  scripts=['bin/fallbeyging'],
  data_files = [
      ('assets',['fallbeyging/assets/processed/bin_words_no_capital_inflection.json']),
      #('target_directory_2', glob('nested_source_dir/**/*', recursive=True)),
  ],
  include_package_data = True,
  packages=['fallbeyging', 'fallbeyging/assets', 'fallbeyging/bin_data', 'fallbeyging/objects'],
  install_requires=[
      'pygame',
  ],
  zip_safe=False)
