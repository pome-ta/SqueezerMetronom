from scene import *


class MyScene(Scene):

  def setup(self):
    pass


if __name__ == '__main__':

  orientation = PORTRAIT
  frame_interval = 1
  show_fps = True

  my_scene = MyScene()

  run(my_scene,
      orientation=orientation,
      frame_interval=frame_interval,
      show_fps=show_fps)

