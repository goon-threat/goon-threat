class Renderable:
  def __init__(self, image, posx, posy, depth=0):
    self.image = image
    self.depth = depth
    self.x = posx
    self.y = posy
    self.w = image.get_width()
    self.h = image.get_height()
