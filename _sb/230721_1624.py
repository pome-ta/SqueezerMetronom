from scene import *


class MyScene(Scene):

  def setup(self):
    pass


if __name__ == '__main__':

  orientation = DEFAULT_ORIENTATION
  frame_interval = 1
  anti_alias = False
  show_fps = False
  multi_touch = True

  my_scene = MyScene()

  run(my_scene)

