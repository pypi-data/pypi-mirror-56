from .fallbeyging import main

def run():
  """Run the main game loop """
  while 1:
    new = main()
    if not new: break