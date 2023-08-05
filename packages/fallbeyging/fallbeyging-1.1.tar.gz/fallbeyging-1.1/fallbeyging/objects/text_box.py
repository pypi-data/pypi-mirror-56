import pygame

pygame.init()

class TextBox:

  def __init__(self, x, y, w, h, text='', font_size=32):
    """
    :param x: top-left x position
    :param y: top-left y position
    :param w: width of the rectangle
    :param h: height of the rectangle
    :param text: text string inside the button
    :param font_size: size of the font of text
    """
    
    # Text
    self.text = str(text)
    self.font = pygame.font.Font(None, font_size)
    self.text_surface = self.font.render(self.text, True, (0, 0, 0))
    self.text_center = self.text_surface.get_rect(center=(x + w/2, y + h/2))

  def render(self, text=''):
    """ Render the new text """

    self.text_surface = self.font.render(str(text), True, (0, 0, 0))

  def draw(self, screen):
    """ Draw text to the screen """

    screen.blit(self.text_surface, self.text_center)
