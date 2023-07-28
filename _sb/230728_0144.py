import scene
import ui

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True
'''
60 は1
120 は0.5

'''


class Tick:

  def __init__(self, bpm: float = 120.0):
    self.bpm: float = bpm
    self.stock_time: float
    self.last_click: int
    self.mul_num: float
    self.set_up()

  def set_up(self):
    self.stock_time = 0.0
    self.last_click = -1
    self.mul_num = (60 * BEAT) / self.bpm

  def increment_time(self, dt: float):
    self.stock_time += dt * self.mul_num

  @property
  def is_click(self) -> bool:
    beat_time = int(self.stock_time)
    if beat_time != self.last_click:
      self.last_click += 1
      return True
    else:
      return False


class Canvas(scene.Scene):

  def __init__(self, bpm: float):
    super().__init__()
    self.bpm = bpm
    self.beat: int = -1
    self.stack_time: float = 0.0

  def setup(self):
    self.ground = scene.Node(parent=self)
    self.tick = Tick(self.bpm)

    position = self.size / 2

    self.label_beat = scene.LabelNode(parent=self.ground, position=position)
    self.label_beat.text = 'あ'

  def update_label(self):
    self.tick.increment_time(self.dt)
    if self.tick.is_click:
      self.beat += 1
      self.label_beat.text = str(self.beat)

  def update(self):
    self.update_label()

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    position = self.size / 2
    self.label_beat.position = position


class View(ui.View):

  def __init__(self, scene_node: scene.Node):
    self.bg_color = 0.88
    self.height_ratio: float = 0.96  # todo: safe area

    self.canvas = scene.SceneView()
    self.canvas.scene = scene_node
    self.canvas.frame_interval = frame_interval
    self.canvas.shows_fps = shows_fps

    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  TITLE = 'title'
  beats_per_minute: float = 120.0

  canvas = Canvas(beats_per_minute)
  view = View(scene_node=canvas)
  view.present(style='fullscreen', orientations=['portrait'])

