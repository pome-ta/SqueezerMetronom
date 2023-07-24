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
    self.setup_dots(w, h)
    self.setup_controller(w, h)
    self.check_play(self.is_play)

  def check_play(self, is_play):
    self.play_btn.text = '⏵' if is_play else '▪︎'
    self.is_play = is_play

  def setup_dots(self, w, h):
    # --- set size
    pos_x = w / 2
    pos_y = h / 1.5
    wrap_w = min(w, h) / 1.5
    wrap_h = max(w, h) / 24

    position = (pos_x, pos_y)
    wrap_path = ui.Path.rect(0, 0, wrap_w, wrap_h)

    self.wrap_dot = scene.ShapeNode(
      path=wrap_path,
      #fill_color='#808080',
      fill_color='clear',
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
        fill_color='clear',
        stroke_color=c[i],
        position=((_gap * i) - _margin, 0),
        parent=self.wrap_dot,
      ) for i in range(BEAT)
    ]

  def setup_controller(self, w, h):
    self.is_play = False
    pos_x = w / 2
    pos_y = h / 2.5

    wp_s = max(w, h) / 8
    wp_path = ui.Path.rect(0, 0, wp_s, wp_s)
    position = (pos_x, pos_y)

    self.wrap_play = scene.ShapeNode(
      path=wp_path,
      fill_color='#808080',
      #fill_color='clear',
      position=position,
      parent=self.ground)

    oval_path = ui.Path.oval(0, 0, wp_s * 0.8, wp_s * 0.8)
    self.oval_wrap = scene.ShapeNode(path=oval_path,
                                     fill_color='#ff00ff',
                                     parent=self.wrap_play)

    # --- set controller
    # ⏵
    # ▪︎
    font = ('Inconsolata', 64)
    self.play_btn = scene.LabelNode(text='',size=self.oval_wrap.size, font=font, parent=self.oval_wrap)
    


if __name__ == '__main__':
  my_scene = MyScene()

  scene.run(my_scene,
            orientation=orientation,
            frame_interval=frame_interval,
            show_fps=show_fps)

