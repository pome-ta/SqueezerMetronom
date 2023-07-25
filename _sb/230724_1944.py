import scene
import ui

frame_interval = 1
shows_fps = True


class Canvas(scene.Scene):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @ui.in_background
  def setup(self):
    self.set_line(128)

  @ui.in_background
  def update(self):
    #print(f'{self.t}')  # 画面左下にlog として表示される
    pass

  def set_line(self, dire):
    w2, h2 = self.size / 2
    path = ui.Path()
    path.move_to(w2 - dire, h2 - dire)
    path.line_to(w2 + dire, h2 + dire)
    line = scene.ShapeNode(parent=self)
    line.path = path
    line.stroke_color = 'red'
    line.position = self.size / 2


def create_button(icon_name):
  button_icon = ui.Image.named(icon_name)
  button = ui.ButtonItem(image=button_icon)
  return button


class View(ui.View):

  def __init__(self, canvas: scene.Scene):
    self.name: str = TITLE
    self.height_ratio: float = 0.96  # todo: safe area

    self.canvas: scene.Scene = canvas
    self.scene_view: ui.View = None

    self.setup_navigationbuttons()
    self.setup_scene()
    self.show_scene()

  def draw(self):
    # todo: init background color
    _, _, w, h = self.frame
    wrap = ui.Path.rect(0, 0, w, h * self.height_ratio)
    #ui.set_color(BG_COLOR)
    wrap.fill()

  def layout(self):
    _, _, w, h = self.frame
    self.scene_view.width = w
    self.scene_view.height = h * self.height_ratio
    self.scene_view.x = (w / 2) - (self.scene_view.width / 2)

  def setup_scene(self):
    self.scene_view = scene.SceneView(frame_interval=frame_interval,
                                      shows_fps=shows_fps,
                                      alpha=0)
    self.scene_view.scene = self.canvas
    self.add_subview(self.scene_view)

  def setup_navigationbuttons(self):
    show_console_icon = 'iob:ios7_download_outline_32'
    show_console_button = create_button(show_console_icon)
    show_console_button.action = self.show_console

    self.right_button_items = [show_console_button]

  @ui.in_background
  def show_scene(self):

    def dissolve():
      self.scene_view.alpha = 1

    ui.animate(dissolve, duration=.24)

  @ui.in_background
  def show_console(self, sender):
    raw_image = self.canvas.view._debug_quicklook_()
    image = ui.Image.from_data(raw_image, 2.0)
    image.show()


if __name__ == '__main__':
  TITLE = 'title'

  canvas = Canvas()
  view = View(canvas)
  view.present(style='fullscreen', orientations=['portrait'])

