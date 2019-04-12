import pygame
from esper import Processor
from goon_threat.component import Renderable

class RenderProcessor(Processor):
  def __init__(self, window, clear_color=(0, 0, 0)):
    super().__init__()
    self.window = window
    self.clear_color = clear_color

  def process(self):
    self.window.fill(self.clear_color) # clear the window

    # This will iterate over every Entity that has this Component, and blit it:
    for ent, rend in self.world.get_component(Renderable):
        self.window.blit(rend.image, (rend.x, rend.y))
    pygame.display.flip() # flip the framebuffers
