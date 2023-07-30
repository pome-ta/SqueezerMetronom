import scene
import ui

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True


class Signal:

  def __init__(self, bpm: float = 120.0, beat: int = 4):
    self.bpm: float = bpm
    self.beat: int = beat  # xxx: 拍数 ?

    self.stock_time: float
    self.last_click: int
    self.mul_num: float
    self.reset()

  def reset(self):
    self.stock_time = 0.0
    self.last_pulse = -1
    self.mul_num = self.bpm / 60

  def increment_time(self, dt: float):
    self.stock_time += dt * self.mul_num

  @property
  def is_pulse(self) -> bool:
    beat_time = int(self.stock_time)
    if beat_time != self.last_pulse:
      self.last_pulse += 1  # xxx: 加算の意味あまりない ? 調整したい
      return True
    else:
      return False


class Lamp(scene.Scene):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.active_color = 'red'
    self.deactive_color = 'blue'
    self.oval_path: ui.Path
    self.dots: list = []

  def setup(self):
    self.ground = scene.Node(parent=self)

  def create_dot(self):
    pass

  def update_size(self):
    w, h = self.size

  def setup_dots(self, w, h):
    pass

  def did_change_size(self):
    self.update_size()


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bpm = bpm
    self.beat: int = -1
    self.stack_time: float = 0.0

  def setup(self):
    self.ground = scene.Node(parent=self)
    self.signal = Signal(self.bpm)
    self.lamp = Lamp(parent=self.ground)

    position = self.size / 2

    self.label_beat = scene.LabelNode(parent=self.ground, position=position)
    self.label_beat.text = 'あ'

  def update_label(self):
    self.signal.increment_time(self.dt)
    if self.signal.is_pulse:
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

    self.canvas = scene.SceneView(scene=scene_node,
                                  frame_interval=frame_interval,
                                  shows_fps=shows_fps)
    '''
    self.canvas.scene = scene_node
    self.canvas.frame_interval = frame_interval
    self.canvas.shows_fps = shows_fps
    '''

    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  TITLE = 'title'
  beats_per_minute: float = 100

  canvas = Canvas(beats_per_minute)
  view = View(scene_node=canvas)
  view.present(style='fullscreen', orientations=['portrait'])

