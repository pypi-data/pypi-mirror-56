import pygame
import random

# Data
from .bin_data.bin_load import BinLoader

# Objects
from .objects.button import Button
from .objects.text_box import TextBox
from .objects.fall_box import FallBox

def main():

  # Global
  screen_w = 800
  screen_h = 600

  # Initialise screen
  screen = pygame.display.set_mode((screen_w, screen_h))
  pygame.display.set_caption('Fallbeygingar leikurinn')

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((250, 250, 250))

  ### Load data ###'

  bin_loader = BinLoader()
  bin_random_words = bin_loader.get_random_words(10)

  ### Game state ###

  new_game = False
  quit_game = False
  # Nr of fallbox in fall_box list
  fall_box_nr = 0
  # Score for current fallbox
  score = 0
  # Total score for all fallbox
  total_score = 0
  # Main menu
  menu_active = False
  # Page nr
  page_nr = 1

  ### Game objects ###

  # Fallbox
  fall_box = list()

  # Populate fall_box
  for key in bin_random_words.keys():
    word = bin_random_words[key]['ord']

    foll = list()
    bmyndir = list()
    begin_list = list()
    
    # Find all foll which aren't empty
    for i, v in enumerate(bin_random_words[key]['bmyndir'].values()):
      if i % 4 == 0:
        if len(v) != 0:
          begin_list.append(i)

    begin = random.choice(begin_list)
    end = begin + 3

    # Append only one type of fall for each word, et, etgr, ft, ftgr
    for i, k in enumerate(bin_random_words[key]['bmyndir'].keys()):

      # Only pick 4 foll, nfet, þfet, þgfet, efet
      if begin <= i and i <= end:
        bmyndir.append(bin_random_words[key]['bmyndir'][k])
        foll.append(k)
      
      # Create a new Fallbox
      if i == end:
        fall_box.append(FallBox(100, 50, word, foll, bmyndir))

        foll = list()
        bmyndir = list()

      # Skip the rest
      if i > end:
        break

  ## Buttons

  # Travel buttons
  button_next = Button(screen_w - 150, screen_h - 100, 125, 50, 'Next')
  button_prev = Button(25, screen_h - 100, 125, 50, 'Previous')

  # Show correct button
  button_show_correct = Button(screen_w/2 - 100, screen_h/2 + 75, 200, 50, 'Show Correct')
  button_show_correct.enable = False
  button_show_correct.is_toggle = True

  # Menu buttons
  button_new = Button(screen_w/2 - 100, screen_h * 1/6, 200, 50, 'New Game')
  button_quit = Button(screen_w/2 - 100, screen_h * 2/6, 200, 50, 'Quit')

  # Textboxes
  page_text = TextBox(10, 10, 100, 40, f'Page: {page_nr}', 32)

  score_text = TextBox(screen_w/2 - 150, screen_h * (2/3) + 45, 300, 50, f'Score: {score}', 50)
  total_score_text = TextBox(screen_w/2 - 150, screen_h * (2/3) + 115, 300, 50, f'Total Score: {total_score}', 50)

  ### Update Game ###

  # Blit the background to the screen
  screen.blit(background, (0,0))
  pygame.display.update()

  clock = pygame.time.Clock()

  # Event loop
  while not quit_game:

    ### Events ###

    # Capture events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
          
          # Next button
          if event.key == pygame.K_RIGHT:
            button_next.normal_event()
          # Previous button
          if event.key == pygame.K_LEFT:
            button_prev.normal_event()

          if event.key == pygame.K_TAB:
            fall_box[fall_box_nr].select_event()
        
        button_next.handle_event(event)
        button_prev.handle_event(event)

        # Menu page or fall page
        if menu_active:
          button_new.handle_event(event)
          button_quit.handle_event(event)
        else:
          fall_box[fall_box_nr].handle_event(event)
          button_show_correct.handle_event(event)

    ### Update ###

    button_next.update()
    button_prev.update()
    
    # Menu page or fall page
    if menu_active:
      button_new.update()
      button_quit.update()
    else:
      fall_box_state = fall_box[fall_box_nr].update()
      button_show_correct.update()

    ### State ###

    # Update renders

    # Score
    score = fall_box[fall_box_nr].score
    score_text.render(f'Score: {score}')

    # Total score
    total_score = 0
    for fb in fall_box:
      total_score += fb.score
    
    total_score_text.render(f'Total Score: {total_score}')

    # Page nr
    page_text.render(f'Page: {page_nr}')

    # Check if all answers have been submited
    if fall_box_state:
      button_show_correct.enable = True
    else:
      button_show_correct.toggle = False
      button_show_correct.enable = False

    # Handle buttons
    
    # Next button was clicked
    if button_next.submited:

      # Go to final screen
      if (fall_box_nr + 1) >= len(fall_box):
        menu_active = True
        page_nr = 0
      else:
        page_nr = page_nr + 1 if not menu_active else 1
        fall_box_nr = fall_box_nr + 1 if not menu_active else 0

        menu_active = False
        button_next.reset()
        button_prev.reset()

    # Previous button was clicked
    if button_prev.submited:

      if (fall_box_nr - 1) < 0:
        menu_active = True
        page_nr = 0
      else:
        page_nr = page_nr - 1 if not menu_active else len(fall_box)
        fall_box_nr = fall_box_nr - 1 if not menu_active else len(fall_box) - 1

        menu_active = False
        button_next.reset()
        button_prev.reset()

    # Quit button was clicked
    if menu_active:
      if button_quit.submited:
        quit_game = True
      
      if button_new.submited:
        quit_game = True
        new_game = True
    
    # Show answer button was clicked
    if button_show_correct.toggle:
      button_show_correct.render('My Answers')
    else:
      button_show_correct.render('Show Correct')

    # Update input boxes
    for input_box in fall_box[fall_box_nr].col_1:
      if button_show_correct.toggle:
        input_box.display_word = ' / '.join([str(word) for word in input_box.correct_words])
        input_box.locked = True
      else:
        input_box.display_word = input_box.word
        input_box.locked = False

    ### Draw ###

    # Draw background
    screen.blit(background, (0, 0))

    # Draw objects
    button_next.draw(screen)
    button_prev.draw(screen)

    page_text.draw(screen)

    if menu_active:
      button_new.draw(screen)
      button_quit.draw(screen)
      total_score_text.draw(screen)
    else:
      fall_box[fall_box_nr].draw(screen)
      button_show_correct.draw(screen)

      score_text.draw(screen)
      total_score_text.draw(screen)

    ### Next cycle ###

    # Update the full display Surface to the screen
    pygame.display.update()
    clock.tick(60)

  if new_game:
    return True

if __name__ == '__main__':
  pygame.init()
  
  while 1:
    new = main()
    if not new: break
  pygame.quit()