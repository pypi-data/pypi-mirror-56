import pygame
import re

from .text_box import TextBox
from .input_box import InputBox

pygame.init()

# Global dimension values
width = 100
height = 38

x_margin = 125
y_margin = 50

class FallBox:

  def __init__(self, x, y, word, col_0_text, col_1_text=['', '', '', '']):
    """
    :param x: top-left x position
    :param y: top-left y position
    :param word: Title
    :param col_0_text: Array of text, NFET, ÞFET, ÞGFET, EFET
    :param col_1_text: Array of text for input boxes
    """

    # Column 0 dimensions
    col_0 = {
      'x': x,
      'y': y + 50,
      'width': width,
      'height': height
    }

    # Column 1 dimensions
    col_1 = {
      'x': x + x_margin,
      'y': y + 50,
      'width': width*4,
      'height': height
    }

    # Score

    # None = not submitted, True = submited correct, False = submited incorrect
    self.correct = [None, None, None, None]
    # Integer score
    self.score = 0

    # Text
    title_font = pygame.font.Font(None, 60)
    self.title = title_font.render(word, True, (0, 0, 0))
    self.title_center = self.title.get_rect(center=(400, y))

    ## Sub title

    # Regex to check what sub texts to display
    r_ft = r'.*ft'
    r_gr = r'.*gr'

    # Fleirtala
    if re.match(r_ft, col_0_text[0], re.IGNORECASE):
      sub_text_1 = 'Fleirtala'
    # Eintala
    else:
      sub_text_1 = 'Eintala'

    # Með greini
    if re.match(r_gr, col_0_text[0], re.IGNORECASE):
      sub_text_2 = 'Með greini'
    # Án greini
    else:
      sub_text_2 = 'Án greini'

    sub_spacing = ' ' * 10
    sub_text = f'{sub_text_1}{sub_spacing}{sub_text_2}'

    sub_title_font = pygame.font.Font(None, 42)
    self.sub_title = sub_title_font.render(sub_text, True, (0, 0, 0))
    self.sub_title_center = self.sub_title.get_rect(center=(400, y+50))

    # Textboxes, NFET, ÞFET, ÞGFET, EFET
    self.col_0 = [
      TextBox(col_0['x'], col_0['y'] + y_margin, col_0['width'], col_0['height'], col_0_text[0]),
      TextBox(col_0['x'], col_0['y'] + y_margin*2, col_0['width'], col_0['height'], col_0_text[1]),
      TextBox(col_0['x'], col_0['y'] + y_margin*3, col_0['width'], col_0['height'], col_0_text[2]),
      TextBox(col_0['x'], col_0['y'] + y_margin*4, col_0['width'], col_0['height'], col_0_text[3])
    ]

    # Input boxes, hestur, hest, hesti, hests
    self.col_1 = [
      InputBox(col_1['x'], col_1['y'] + y_margin, col_1['width'], col_1['height'], col_1_text[0]),
      InputBox(col_1['x'], col_1['y'] + y_margin*2, col_1['width'], col_1['height'], col_1_text[1]),
      InputBox(col_1['x'], col_1['y'] + y_margin*3, col_1['width'], col_1['height'], col_1_text[2]),
      InputBox(col_1['x'], col_1['y'] + y_margin*4, col_1['width'], col_1['height'], col_1_text[3])
    ]

  def select_event(self):
    """ Special event handler to handle input box selection with the <tab>
    key, it loops around 
    """

    select_ib = 0
    for i, ib in enumerate(self.col_1):
      
      # Deactivate current inputbox and activate the next one, loops the array
      if ib.active:
        ib.deactivate()
        select_ib = i+1 if i+1 < len(self.col_1) else 0
    
    self.col_1[select_ib].activate()

  def handle_event(self, event):
    """ Pass on event handling to each input box """

    for row in self.col_1:
      row.handle_event(event)

  def update(self):
    """ Update with score and handle when all answers have been submited"""
    
    # Update the None array with True or False, depending on the answer
    for i, row in enumerate(self.col_1):
      row.update()
      # Check if answer is submited
      if row.submited:
        self.correct[i] = row.correct
    
    # Update total score for the current fall box
    self.score = sum(filter(None, self.correct))

    # All answers have been submited
    if not None in self.correct:
      return True

    return False


  def draw(self, screen):
    """ Draw the title, subtitle, 4 text boxes and 4 input boxes """

    # Blit title and subtitle
    screen.blit(self.title, self.title_center)
    screen.blit(self.sub_title, self.sub_title_center)

    # Blit the text boxes
    for row in self.col_0:
      row.draw(screen)

    # Blit the input boxes
    for row in self.col_1:
      row.draw(screen)