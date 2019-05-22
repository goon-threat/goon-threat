# Alright guys, I made a guy move, rotate, jump, and idle, actually using esper this time
# Can we make this our master file? Happy to walk anyone through how it works

# Also, all the components and processors can easily be moved to different files
# I want to keep them in the main file until we all know what they do and how to use them
# Then we can migrate

# I made the jump function work before I figured out how the components and processors worked
# It could probably be reworked, especially once we start incorporating platforms and such



import pygame
from goon_threat import esper



FPS = 60
RESOLUTION = 720, 480


##################################
#  Defining Components
#  These will all be in different files eventually
##################################
class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Renderable:
  def __init__(self, images, posx, posy):
    self.images=images
    self.image = images[0]
    self.x = posx
    self.y = posy
    self.w = images[0].get_width()
    self.h = images[0].get_height()
    self.orientation="Right"

    self.libraries=[]
    self.idling=True

  def set_orientation(self,orientation):
    self.orientation = orientation

  def set_idling(self,idling):
    self.idling=idling

  def set_idle_image(self, phase):
    self.image=self.images[phase]
    if self.orientation=="Left":
      pygame.transform.flip(self.image,True,False)
    self.w=self.images[phase].get_width()
    self.h=self.images[phase].get_height()

  def add_image_library(self,library):#add a list of images to a renderable object for different purposes
    self.libraries.append(library)

  def set_other_image(self,index,phase):
    this_library=self.libraries[index]
    self.image=this_library[phase]




#######################################################
#  Defining processors
#  These will also move to different files eventually
#######################################################
class MovementProcessor(esper.Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.phase = 0

    def set_phase(self, current_frame):
      if current_frame < 10:
        self.phase = 0
      elif current_frame < 20:
        self.phase = 1
      elif current_frame < 30:
        self.phase = 2
      elif current_frame < 40:
        self.phase = 3
      elif current_frame < 50:
        self.phase = 4
      else:
        self.phase = 5

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            # Update the Renderable Component's position by it's Velocity:
            rend.x += vel.x
            rend.y += vel.y
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)

            rend.set_other_image(0,self.phase)

class IdleProcessor(esper.Processor):
  def __init__(self,window):
    super().__init__()
    self.window = window
    self.phase=0
    self.idling=True

  def set_phase(self,current_frame):
    if current_frame<15:
      self.phase=0
    elif current_frame<30:
      self.phase=1
    elif current_frame<45:
      self.phase=2
    else:
      self.phase=3


  def process(self):
    for ent, (rend) in self.world.get_component(Renderable):
      if rend.idling:
        rend.set_idle_image(self.phase)



class RenderProcessor(esper.Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(Renderable):
            if rend.orientation=="Right":
              self.window.blit(rend.image, (rend.x, rend.y))
            elif rend.orientation=="Left":
              self.window.blit(pygame.transform.flip(rend.image,True,False), (rend.x,rend.y))
        # Flip the framebuffers
        pygame.display.flip()


################################
#  launching the program
################################
def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Goon Threat")
    clock = pygame.time.Clock()
    current_frame=0
    pygame.key.set_repeat(1, 1)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = esper.World()
    player = world.create_entity()
    world.add_component(player, Velocity(x=0, y=0))

    player_idle_images=[pygame.image.load('images/idle-2-00.png'), pygame.image.load('images/idle-2-01.png'),
                  pygame.image.load('images/idle-2-02.png'), pygame.image.load('images/idle-2-03.png'),]
    player_moving_images=[pygame.image.load('images/run-00.png'), pygame.image.load('images/run-01.png'),
                          pygame.image.load('images/run-02.png'), pygame.image.load('images/run-03.png'),
                          pygame.image.load('images/run-04.png'), pygame.image.load('images/run-05.png')]
    world.add_component(player, Renderable(player_idle_images, posx=100, posy=700))
    world.component_for_entity(player, Renderable).add_image_library(player_moving_images)


    # Instantiating the processors, and adding them to the world
    render_processor = RenderProcessor(window=window)
    idle_processor = IdleProcessor(window=window)
    movement_processor = MovementProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])
    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(idle_processor)


    def jump(frame):
        Frames = [-5,-5,-5,-5,-5,-5,-4,-3,-2,-2,-2,-1,-1,0,0,0,0,1,1,2,2,2,3,4,5,5,5,5,5,5] #I am aware this is ugly
        world.component_for_entity(player, Velocity).y = Frames[frame]


    running = True
    jumping = False
    jump_phase = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                world.component_for_entity(player, Renderable).set_idling(False)
                if event.key == pygame.K_LEFT:
                    world.component_for_entity(player, Renderable).set_orientation("Left")
                    world.component_for_entity(player, Velocity).x = -3
                elif event.key == pygame.K_RIGHT:
                    world.component_for_entity(player, Renderable).set_orientation("Right")
                    world.component_for_entity(player, Velocity).x = 3
                elif event.key == pygame.K_UP:
                    if not jumping:
                        jumping = True


                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    world.component_for_entity(player, Velocity).x = 0
                    world.component_for_entity(player, Renderable).set_idling(True)
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    world.component_for_entity(player, Velocity).y = 0
        if jumping:
            jump(jump_phase)
            jump_phase += 1 #jump_phase is the number of frames that have passed since the start of the jump
            if jump_phase == 30: #in this case, the jump is 30 frames long
                jumping = False
                jump_phase=0

        current_frame += 1
        if current_frame == 60:
          current_frame = 0

        idle_processor.set_phase(current_frame)
        movement_processor.set_phase(current_frame)

        # A single call to world.process() will update all Processors:
        world.process()
        clock.tick(FPS)

if __name__ == "__main__":
    run()
    pygame.quit()
