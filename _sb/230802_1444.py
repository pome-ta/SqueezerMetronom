import scene
import ui

from objc_util import ObjCClass

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


class Feedback:

  def __init__(self):
    self.__strong = self.__get_feedback_generator(4)
    self.__weak = self.__get_feedback_generator(0)

  @property
  def strong(self):
    return self.__strong.impactOccurred()

  @property
  def weak(self):
    return self.__weak.impactOccurred()

  def __get_feedback_generator(self, style: int = 0) -> ObjCClass:
    """
    call feedback ex:
    `UIImpactFeedbackGenerator.impactOccurred()`
    """
    '''
    https://developer.apple.com/documentation/uikit/uiimpactfeedbackgenerator/feedbackstyle
      
      case light = 0
      case medium = 1
      case heavy = 2
      case soft = 3
      case rigid = 4
    '''
    UIImpactFeedbackGenerator = ObjCClass('UIImpactFeedbackGenerator').new()
    UIImpactFeedbackGenerator.prepare()
    UIImpactFeedbackGenerator.initWithStyle_(style)
    return UIImpactFeedbackGenerator


class ClickSound:

  def __init__(self):
    pass


class Lamp(scene.Node):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.wrap: scene.ShapeNode
    self.dots: list
    self.line_width: int = 4

    #color_tone = 'maroon'
    color_tone = '#808080'
    self.active_is = {
      'fill_color': color_tone,
      'stroke_color': color_tone,
    }
    self.deactive_is = {
      'fill_color': 'clear',
      'stroke_color': color_tone,
    }

    self.set_up()

  def set_up(self):
    self.wrap = scene.ShapeNode(parent=self,
                                fill_color='clear',
                                stroke_color='clear')
    self.dots = [self.__create_dot() for _ in range(BEAT)]

    self.change_size_position()
    self.update_status(0)

  def __create_dot(self) -> scene.ShapeNode:
    shape_node = scene.ShapeNode(parent=self.wrap)
    return shape_node

  def update_status(self, active_index: int):
    for n, dot in enumerate(self.dots):
      if n == active_index:
        dot.fill_color = self.active_is['fill_color']
        dot.stroke_color = self.active_is['stroke_color']
      else:
        dot.fill_color = self.deactive_is['fill_color']
        dot.stroke_color = self.deactive_is['stroke_color']

  def change_size_position(self):
    w, h = self.parent.size

    pos_x = w / 2
    pos_y = h / 1.5
    wrap_w = min(w, h) / 1.5
    wrap_h = max(w, h) / 24

    self.wrap.path = ui.Path.rect(0, 0, wrap_w, wrap_h)
    self.wrap.position = (pos_x, pos_y)

    oval_path = ui.Path.oval(0, 0, wrap_h, wrap_h)
    oval_path.line_width = self.line_width

    ovals_w = wrap_w - wrap_h - (self.line_width / 2)
    span = ovals_w / (BEAT - 1)
    st_point = ovals_w / 2

    for n, dot in enumerate(self.dots):
      _x = (span * n) - st_point
      dot.path = oval_path
      dot.position = (_x, 0.0)


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bpm = bpm
    self.beat: int = -1
    self.beat_index: int = 0

  def setup(self):
    self.signal = Signal(self.bpm)
    self.lamp = Lamp(parent=self)
    self.feedback = Feedback()

    position = self.size / 2

    self.label_beat = scene.LabelNode(parent=self, position=position)
    self.label_beat.text = 'あ'

  def update_label(self):
    self.label_beat.text = f'{self.bpm}\n{str(self.beat)}'

  def update(self):
    self.signal.increment_time(self.dt)
    if self.signal.is_pulse:
      self.beat += 1
      self.beat_index = self.beat % BEAT
      self.update_label()
      self.lamp.update_status(self.beat_index)
      self.feedback.weak if self.beat_index else self.feedback.strong

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    position = self.size / 2
    self.label_beat.position = position
    self.lamp.change_size_position()


class View(ui.View):

  def __init__(self, scene_node: scene.Node):
    self.bg_color = 0.88
    self.height_ratio: float = 0.96  # todo: safe area

    self.canvas = scene.SceneView(scene=scene_node,
                                  frame_interval=frame_interval,
                                  shows_fps=shows_fps)
    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  TITLE = 'title'
  beats_per_minute: float = 112.0

  canvas = Canvas(beats_per_minute)
  view = View(scene_node=canvas)

  view.present(style='fullscreen', orientations=['portrait'])
  #view.present(style='fullscreen')

