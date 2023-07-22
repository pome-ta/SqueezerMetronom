from scene import Scene, Node, run, PORTRAIT
import ui

orientation = PORTRAIT
frame_interval = 1
show_fps = True


class MyScene(Scene):

  def setup(self):
    self.ground = Node(parent=self)
    w = self.size.width
    h = self.size.height
    dots_rect = ui.Path


if __name__ == '__main__':
  my_scene = MyScene()

  run(my_scene,
      orientation=orientation,
      frame_interval=frame_interval,
      show_fps=show_fps)

