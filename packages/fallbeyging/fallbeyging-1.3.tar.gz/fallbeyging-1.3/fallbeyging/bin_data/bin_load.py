import os
import json
import random
import zipfile

class BinLoader:

  def __init__(self):
    """ Read read_path into memory """

    self.base_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    self.json_path = os.path.join('assets', 'processed', 'bin_words_no_capital_inflection.json')
    self.read_path = os.path.join(self.base_path, self.json_path)
    
    self.json = {}

    # If the json file is within zipped
    if self.base_path.endswith('.zip'):

      with zipfile.ZipFile(self.base_path, "r") as z:
        with z.open(self.json_path) as f:
          data = f.read()
          self.json = json.loads(data.decode("utf-8"))
    # If the json file is in a normal directory
    else:
      with open(self.read_path, 'r') as f:
        self.json = json.load(f)

  def get_random_words(self, n):
    """ Get a random sample of n words from the bin_list
    :param n: Number of words
    :return: dictionary with n random words
    """

    rand_list = random.choices(list(self.json.items()), k=n)

    return dict(rand_list)

  def get_word_by_guid(self, word='6a09e6c50425a7a1197f0e7c05216662'):
    """ Get specific word by guid """

    return {word: self.json[word]}

