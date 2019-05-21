class Renderable:
  def __init__(self, images, posx, posy, depth=0):
    self.image = images[0]
    self.depth = depth
    self.x = posx
    self.y = posy
    self.w = images[0].get_width()
    self.h = images[0].get_height()

