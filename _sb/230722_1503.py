#from scene import Scene, Node, ShapeNode, run, PORTRAIT
import scene
import ui

orientation = scene.PORTRAIT
frame_interval = 1
show_fps = True


class MyScene(scene.Scene):

  def setup(self):
    self.ground = scene.Node(parent=self)
    w = self.size.width
    h = self.size.height

    # --- set size
    pos_x = w / 2
    pos_y = h / 1.5
    wrap_w = min(w, h) / 1.5
    wrap_h = max(w, h) / 16

    position = (pos_x, pos_y)
    wrap_rect = ui.Path.rect(0, 0, wrap_w, wrap_h)
    self.wrap = scene.ShapeNode(path=wrap_rect,
                                position=position,
                                parent=self.ground)
    #self.ground.add_child(self.wrap)


if __name__ == '__main__':
  my_scene = MyScene()

  scene.run(my_scene,
            orientation=orientation,
            frame_interval=frame_interval,
            show_fps=show_fps)

