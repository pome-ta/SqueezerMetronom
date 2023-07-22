from scene import Scene, Node, ShapeNode, run, PORTRAIT
import ui

orientation = PORTRAIT
frame_interval = 1
show_fps = True


class MyScene(Scene):

  def setup(self):
    self.ground = Node(parent=self)
    w = self.size.width
    h = self.size.height
    wrap_rect = ui.Path.rect(0, 0, 100, 200)
    self.wrap = ShapeNode(wrap_rect, parent=self.ground)
    #self.ground.add_child(self.wrap)


if __name__ == '__main__':
  my_scene = MyScene()

  run(my_scene,
      orientation=orientation,
      frame_interval=frame_interval,
      show_fps=show_fps)

