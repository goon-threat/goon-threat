import pygame
import esper

FPS = 60
RESOLUTION = 720, 480

def run():
  pygame.display.set_mode(RESOLUTION)
  pygame.display.set_caption("Esper Pygame example")
  clock = pygame.time.Clock()
  pygame.key.set_repeat(1, 1)

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      clock.tick(FPS)
