import bin_data
import objects
from .game import main

def run():
  """Run the main game loop """
  while 1:
    new = main()
    if not new: break