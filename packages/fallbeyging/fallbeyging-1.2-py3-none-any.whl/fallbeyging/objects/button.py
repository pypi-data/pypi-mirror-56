import pygame

pygame.init()

# Colours
col_enabled = pygame.Color(125, 255, 0)
col_disabled = pygame.Color(255, 125, 0)

# Button clicked
col_active = pygame.Color(0, 255, 0)

# Toggle
col_toggle_false = pygame.Color(0, 0, 255)
col_toggle_true = pygame.Color(0, 125, 255)

col_font = pygame.Color(0, 0, 0)

class Button:

  def __init__(self, x, y, w, h, text=''):
    """
    :param x: top-left x position
    :param y: top-left y position
    :param w: width of the rectangle
    :param h: height of the rectangle
    :param text: text string inside the button
    """
    
    self.rect = pygame.Rect(x, y, w, h)

    # Type
    self.is_toggle = False

    # Visual
    self.color = col_enabled
    
    # Button text
    self.text = ''
    self.font = pygame.font.Font(None, 32)
    self.text_surface = self.font.render(text, True, col_font)
    self.text_center = self.text_surface.get_rect(center=(x + w/2, y + h/2))

    # Triggers
    self.enable = True
    self.submited = False
    self.toggle = False

  def normal_event(self):
    """ Handle normal button event """

    if self.enable:
      self.submited = True
      self.color = col_active

  def toggle_event(self):
    """ Handle toggle button event """

    if self.enable:
      self.submited = not self.submited
      self.toggle = not self.toggle

  def render(self, text):
    """ Render the new text """

    self.text_surface = self.font.render(text, True, col_font)

  def reset(self):
    """ Reset the object """

    self.color = col_enabled
    self.submited = False
    self.enable = True

  def handle_event(self, event):
    """ Handles mouse click event and 
    left and right arrow key event
    """

    # Check if button is enabled
    if self.enable:
      
      # Check mouse click
      if event.type == pygame.MOUSEBUTTONDOWN:
        
        # Handle toggle buttons
        if self.is_toggle:
          # User clicked in input box
          if self.rect.collidepoint(event.pos):
            self.toggle_event()
        
        # Handle normal buttons
        else:
          # User clicked in input box
          if self.rect.collidepoint(event.pos):
            self.normal_event()

  def update(self):
    """ Update colours """

    # Disable colour
    if not self.enable:
      self.color = col_disabled
    else:
      # Toggle colour
      if self.is_toggle:
        self.color = col_toggle_true if self.toggle else col_toggle_false
      # Normal colour
      else:
        self.color = col_enabled

  def draw(self, screen):
    """ Draw text and rectangle to the screen """

    pygame.draw.rect(screen, self.color, self.rect, 0)
    screen.blit(self.text_surface, self.text_center)