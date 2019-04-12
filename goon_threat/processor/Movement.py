from esper import Processor
from goon_threat.component import Renderable, Velocity

class MovementProcessor(Processor):
  def __init__(self, minx, maxx, miny, maxy):
    super().__init__()
    self.minx = minx
    self.maxx = maxx
    self.miny = miny
    self.maxy = maxy

  def process(self):
    for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
        # Update the Renderable Component's position by its Velocity:
        rend.x += vel.x
        rend.y += vel.y

        # Adjust the position back inside screen boundaries if the entity tries to go outside:
        rend.x = max(self.minx, rend.x)
        rend.y = max(self.miny, rend.y)
        rend.x = min(self.maxx - rend.w, rend.x)
        rend.y = min(self.maxy - rend.h, rend.y)
