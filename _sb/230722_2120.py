import scene
import ui

BEAT: int = 4
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
    wrap_h = max(w, h) / 24

    position = (pos_x, pos_y)
    wrap_path = ui.Path.rect(0, 0, wrap_w, wrap_h)
    # xxx: 透過できないかも
    self.wrap = scene.ShapeNode(path=wrap_path,
                                fill_color='#808080',
                                position=position,
                                parent=self.ground)

    # --- set dots
    
    c = ['#00ffff', '#00ff00', '#ff0000', '#ffff00']
    oval_path = ui.Path.oval(0, 0, wrap_h, wrap_h)

    _hd = wrap_h / 2
    _gap = ((wrap_w + _hd) / BEAT) + _hd
    _margin = wrap_w / 2

    self.dots = [
      scene.ShapeNode(
        path=oval_path,
        fill_color=c[i],
        position=((_gap * i) - _margin, 0),
        parent=self.wrap,
      ) for i in range(BEAT)
    ]
    
    # --- set controller
    
    


if __name__ == '__main__':
  my_scene = MyScene()

  scene.run(my_scene,
            orientation=orientation,
            frame_interval=frame_interval,
            show_fps=show_fps)

