import os
import re
import json
from urllib import request, parse

class BinBmyndir:

  def __init__(self, write_path, word_list):
    self.word_list = word_list

    # Create an exclusive file
    self.file = write_path
    with open(self.file, 'x') as f:
      json.dump({}, f, ensure_ascii=False, indent=2)

    # Number of requests between saves
    self.num_req = 5000
    # Data in memory, before it's saved to file
    self.json = dict()

    # Regex
    self.r_1 = r'.*[0-9]+'

    # API
    self.base_url = 'https://bin.arnastofnun.is/api/ord'
    self.type = 'no'

    # Start getting the data from the api
    self.__req_all()

  def __add_data(self, data):

    print(data[0]['ord'])

    # Json data structure
    self.json[data[0]['guid']] = {
      'ord': data[0]['ord'],
      'kyn': data[0]['kyn'],
      'bmyndir': {
        'NFET': [],
        'ÞFET': [],
        'ÞGFET': [],
        'EFET': [],
        'NFETgr': [],
        'ÞFETgr': [],
        'ÞGFETgr': [],
        'EFETgr': [],
        'NFFT': [],
        'ÞFFT': [],
        'ÞGFFT': [],
        'EFFT': [],
        'NFFTgr': [],
        'ÞFFTgr': [],
        'ÞGFFTgr': [],
        'EFFTgr': [],
      }
    }

    # Run through the words föll
    for fall in data[0]['bmyndir']:
      # Additional fall, 'NFET2'
      if re.match(self.r_1, fall['g']):
        self.json[data[0]['guid']]['bmyndir'][fall['g'][:-1]].append(fall['b'])
      # Add fall to word
      else:
        self.json[data[0]['guid']]['bmyndir'][fall['g']].append(fall['b'])

  def __api_word(self, word):
    # Parse word to avoid encoding issues
    parsed_word = parse.quote(word)
    url = f'{self.base_url}/{self.type}/{parsed_word}'

    # Request
    res = request.urlopen(url)
    data = json.loads(res.read().decode('UTF-8'))

    return data

  def __api_guid(self, guid):
    # Parse word to avoid encoding issues
    parsed_guid = parse.quote(guid)
    url = f'{self.base_url}/{parsed_guid}'

    # Request
    res = request.urlopen(url)
    data = json.loads(res.read().decode('UTF-8'))

    return data

  def __save(self):
    # Open json file to append to it
    with open(self.file, 'r') as f:
      data = json.load(f)

      data.update(self.json)

    # Write to json file
    with open(self.file, 'w') as f:
      json.dump(data, f, ensure_ascii=False, indent=2)

    # Reset json data after it has been save to the file
    self.json = dict()

  def __req_list(self, word_list):
    
    for word in word_list:
      data = self.__api_word(word)

      # Response is empty
      if type(data) is dict:
        continue

      # Response is empty
      if len(data) == 0:
        continue

      # Response returned multiple variation of a word
      if len(data) >= 2:
        # Iterate through all the variances
        for d in data:
          data = self.__api_guid(d['guid'])
          self.__add_data(data)
        
        continue

      # Response didn't return key: 'bmyndir'
      if 'bmyndir' not in data:
        data = self.__api_guid(data[0]['guid'])

      self.__add_data(data)

  def __req_all(self):

    for i in range(0, len(self.word_list), self.num_req):

      # Process words into a dict of dict of list
      self.__req_list(self.word_list[i:i+self.num_req])

      # Write words to a csv file
      self.__save()

      print('-' * 40 + 'FILE SAVED' + '-' * 40)


##################

if __name__ == '__main__':

  def read_file(file_path):
    """ Read contents of file, each line as an element in a list
    :param file_path: Real path to file
    :return: a list of words
    """
    with open(file_path, 'r') as words_file:
      word_list = [line[:-1] for line in words_file]

    return word_list

  # Paths
  read_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'words', 'bin_words_no_capital.txt'))
  write_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'processed', 'bin_words_no_capital_inflection.json'))

  w_list = read_file(read_path)

  BinBmyndir(write_path, w_list)