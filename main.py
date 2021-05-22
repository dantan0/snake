import pygame
import time
import random

pygame.init()

screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Snake game')

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

clock = pygame.time.Clock()

class SnakeState():
  def __init__(self):
    self.snake_list = []
    self.snake_block = 10
    self.snake_length = 1
    self.snake_head = [screen_width / 2, screen_height / 2]
    self.change = [0, 0]
    self.food = [screen_width / 2 + 50, screen_height / 2 + 50]
  
  def move_snake(self, event):
    if event.key == pygame.K_LEFT:
      self.change[0] = -10
      self.change[1] = 0
    elif event.key == pygame.K_RIGHT:
      self.change[0] = 10
      self.change[1] = 0
    elif event.key == pygame.K_UP:
      self.change[1] = -10
      self.change[0] = 0
    elif event.key == pygame.K_DOWN:
      self.change[1] = 10
      self.change[0] = 0
    
  def set_head(self):
    self.snake_head[0] += self.change[0]
    self.snake_head[1] += self.change[1]
    self.snake_list.append([self.snake_head[0], self.snake_head[1]])

    # delete the tail
    if len(self.snake_list) > self.snake_length:
      del self.snake_list[0]
  
  def draw_snake(self):
    for x in self.snake_list:
      pygame.draw.rect(screen, black, [x[0], x[1], self.snake_block, self.snake_block])

  def draw_food(self):
    pygame.draw.rect(screen, blue, [self.food[0], self.food[1], self.snake_block, self.snake_block])
  
  def detect_boundary(self):
    return self.snake_head[0] < 0 or self.snake_head[0] > screen_width or self.snake_head[1] < 0 or self.snake_head[1] > screen_height

  def detect_food(self):
    return self.snake_head[0] == self.food[0] and self.snake_head[1] == self.food[1]

  def reset_food(self):
    # reset food if snake is at food
    if self.detect_food():
      self.food[0] = round(random.randrange(0, screen_width - self.snake_block) / 10.0) * 10.0
      self.food[1] = round(random.randrange(0, screen_height - self.snake_block) / 10.0) * 10.0
      self.snake_length += 1
  
  def update_state(self):
    self.set_head()
    self.draw_food()
    self.draw_snake()
    self.reset_food()

class Game():
  def message(self, msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width/5, screen_height/5])

  def game_loop(self):
    game_over = False
    game_close = False

    s = SnakeState()

    while not game_over:
      while game_close == True:
        screen.fill(white)
        self.message("You Lost! Press Q-Quit or C-Play Again", red)
        pygame.display.update()

        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
              game_over = True
              game_close = False
            if event.key == pygame.K_c:
              self.game_loop()
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          game_over = True
        if event.type == pygame.KEYDOWN:
          s.move_snake(event)

      # when snake hits boundaries, then it's game over
      if s.detect_boundary():
        game_close = True

      screen.fill(white)
      s.update_state()
      pygame.display.update()
      clock.tick(15)

    pygame.quit()
    quit()

game = Game()
game.game_loop()