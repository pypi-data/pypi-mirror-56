import pygame

pygame.init()

# Colours

col_inactive = pygame.Color('lightskyblue3')
col_active = pygame.Color(0, 0, 255)

col_correct = pygame.Color(0, 255, 0)
col_incorrect = pygame.Color(255, 0, 0)

class InputBox:

  def __init__(self, x, y, w, h, words=[]):
    """
    :param x: top-left x position
    :param y: top-left y position
    :param w: width of the rectangle
    :param h: height of the rectangle
    :param words: Correct words for this input box, to check for answer
    """

    self.rect = pygame.Rect(x, y, w, h)

    # Logic
    self.correct_words = words
    self.correct = False

    # Visual
    self.color = col_inactive
    self.display_word = ''
    
    # Input word
    self.word = ''
    self.font = pygame.font.Font(None, 38)
    self.word_surface = self.font.render('', True, (0, 0, 0))

    # Triggers
    self.active = False
    self.submited = False

    # Lock input in while showing answer
    self.locked = False

  def check(self):
    """ Checks if the submitted answer is correct """

    # Word is correct
    if self.word in self.correct_words:
      self.color = col_correct
      self.correct = True
    # Word is incorrect
    else:
      self.color = col_incorrect

    self.submited = True

  def activate(self):
    """ Activates the button """

    if not self.submited and not self.locked:
      self.active = not self.active
      self.color = col_active

  def deactivate(self):
    """ Deactivates the button """

    if not self.submited and not self.locked:
      self.active = False
      self.color = col_inactive

  def handle_event(self, event):
    """ Handles mouse click event, activates the input box,
    keydown event saves input text, <tab> is ignored and <enter>
    submits the answer
    """

    # Check if answer has been submited
    if not self.submited and not self.locked:

      # Check mouse click
      if event.type == pygame.MOUSEBUTTONDOWN:
        # User clicked in input box
        if self.rect.collidepoint(event.pos):
            self.activate()
        else:
            self.deactivate()
      # Check key press
      if event.type == pygame.KEYDOWN:
        # Check if input box is selected
        if self.active:
          
          # Enter
          if event.key == pygame.K_RETURN:
            self.check()
          
          # Backspace
          elif event.key == pygame.K_BACKSPACE:
              self.word = self.word[:-1]
          
          # Tab
          elif event.key == pygame.K_TAB:
            pass

          # All other keys
          else:
              self.word += event.unicode
          
          # Render the new word
          self.display_word = self.word
          self.word_surface = self.font.render(self.display_word, True, (0, 0, 0))

          # Limit word length
          if self.word_surface.get_width() >= self.rect.w * 0.9:
            self.word = self.word[:-1]

  def update(self):
    """ Update with input text """

    self.word_surface = self.font.render(self.display_word, True, (0, 0, 0))

  def draw(self, screen):
    """ Draw text and rectangle to the screen """

    screen.blit(self.word_surface, (self.rect.x+5, self.rect.y+5))
    pygame.draw.rect(screen, self.color, self.rect, 4)