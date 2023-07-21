from scene import *


class MyScene(Scene):

  def setup(self):
    pass


#settings = {show_fps=False}
settings = {
  'show_fps': False,
}
'''
run(
  MyScene(),
  frame_interval=0,
  show_fps=True,
)
'''
#settings = [show_fps=False]
orientation=DEFAULT_ORIENTATION
frame_interval=1
anti_alias=False
show_fps=False
multi_touch=True

my_scene = MyScene()
run(my_scene, *settings)
