import scene
import ui

from objc_util import ObjCClass, uiimage_to_png

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True

TINT_COLOR = '#808080'

UIImage = ObjCClass('UIImage')
UIColor = ObjCClass('UIColor')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')


def configuration_by_applying_configuration(
    applys: list) -> UIImageSymbolConfiguration:
  _conf = UIImageSymbolConfiguration.defaultConfiguration()
  for apply in applys:
    _conf = _conf.configurationByApplyingConfiguration_(apply)
  return _conf


def get_symbo_icon(symbol_name: str, point_size: float = 256.0) -> ui.Image:

  size = UIImageSymbolConfiguration.configurationWithPointSize_(point_size)
  color = UIImageSymbolConfiguration.configurationPreferringMonochrome()

  conf = configuration_by_applying_configuration([size, color])

  # todo: `scene.Texture` で着色
  tint_color = UIColor.whiteColor()
  '''
  case automatic = 0
  case alwaysOriginal = 1
  case alwaysTemplate = 2
  '''

  ui_image = UIImage.systemImageNamed_withConfiguration_(
    symbol_name, conf).imageWithTintColor_renderingMode_(tint_color, 1)

  png_bytes = uiimage_to_png(ui_image)
  png_img = ui.Image.from_data(png_bytes, 2)
  return png_img


class Signal:

  def __init__(self, bpm: float = 120.0, beat: int = 4):
    self.bpm: float = bpm
    self.beat: int = beat  # xxx: 拍数 ?

    self.stock_time: float
    self.past_pulse: int
    self.mul_num: float
    self.reset()

  def reset(self):
    self.stock_time = 0.0
    self.past_pulse = -1
    self.mul_num = self.bpm / 60

  def increment_time(self, dt: float):
    self.stock_time += dt * self.mul_num

  @property
  def is_pulse(self) -> bool:
    beat_time = int(self.stock_time)
    if beat_time != self.past_pulse:
      self.past_pulse += 1  # xxx: 加算の意味あまりない ? 調整したい
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


class PlayButton(scene.Node):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.wrap: scene.ShapeNode
    self.circle: scene.ShapeNode
    self.icon_shape: scene.ShapeNode
    self.icon: scene.SpriteNode
    self.play_texture: scene.Texture
    self.stop_texture: scene.Texture

    self.is_play: bool = False
    self.line_width: int = 4
    self.set_up()

  def set_up(self):
    self.wrap = scene.ShapeNode(parent=self,
                                fill_color='clear',
                                stroke_color='clear')
    self.circle = scene.ShapeNode(parent=self.wrap,
                                  fill_color='clear',
                                  stroke_color=TINT_COLOR)
    self.icon_shape = scene.ShapeNode(parent=self.circle,
                                      fill_color='clear',
                                      stroke_color='clear')
    # xxx: debug
    self.wrap.stroke_color = 'cyan'
    #self.icon_shape.stroke_color = 'maroon'

    self.is_play = False
    self.__create_icon()
    self.change_size_position()

  def __create_icon(self):
    play_symbo = get_symbo_icon('play.fill')
    stop_symbo = get_symbo_icon('stop.fill')
    #stop_symbo = get_symbo_icon('play.fill')
    #stop_symbo = get_symbo_icon('cable.connector.horizontal')
    #stop_symbo = get_symbo_icon('cable.connector')

    self.play_texture = scene.Texture(play_symbo)
    self.stop_texture = scene.Texture(stop_symbo)

    self.icon = scene.SpriteNode(parent=self.icon_shape)
    self.icon.color = TINT_COLOR
    self.select_icon()

  def select_icon(self):
    # xxx: `@property` するか？
    selected_texture = self.play_texture if self.is_play else self.stop_texture
    self.icon.texture = selected_texture

  def change_size_position(self):
    w, h = self.parent.size
    pos_x = w / 2
    pos_y = h / 2.5
    wrap_w = wrap_h = min(w, h) / 2
    self.wrap.path = ui.Path.rect(0, 0, wrap_w, wrap_h)
    self.wrap.position = (pos_x, pos_y)

    circle_path = ui.Path.oval(0, 0, wrap_w, wrap_h)
    circle_path.line_width = self.line_width
    self.circle.path = circle_path

    #sq_size = min(self.circle.size)  # * 0.64
    #sq_size = min(self.circle.size) / 2**0.5  # `sqrt(2)`
    # todo: 正円に接する正四角形の長さ
    sq_size = min(self.circle.size) / pow(2, 0.5)
    self.icon_shape.path = ui.Path.rect(0, 0, sq_size, sq_size)

    selected_texture = self.play_texture if self.is_play else self.stop_texture
    t_w, t_h = selected_texture.size
    asp = sq_size / max(t_w, t_h)
    self.icon.texture = selected_texture
    self.icon.size = (t_w * asp, t_h * asp)

    #print(t_w)


class Lamp(scene.Node):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.wrap: scene.ShapeNode
    self.dots: list
    self.line_width: int = 4

    self.active_is = {
      'fill_color': TINT_COLOR,
      'stroke_color': TINT_COLOR,
    }
    self.deactive_is = {
      'fill_color': 'clear',
      'stroke_color': TINT_COLOR,
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
    self.is_play: bool = False
    self.past_play: bool  # xxx: なんだけっけこれ

  def setup(self):
    self.is_play = False
    self.signal = Signal(self.bpm)
    self.lamp = Lamp(parent=self)
    self.play_botton = PlayButton(parent=self)
    self.feedback = Feedback()

    position = self.size / 2

    self.label_beat = scene.LabelNode(parent=self, position=position)
    self.label_beat.text = 'あ'
    self.update_label()

  def update_label(self):
    self.label_beat.text = f'{self.bpm}\n{str(self.beat)}'

  def update(self):
    if not (self.is_play):
      return
    self.signal.increment_time(self.dt)
    if self.signal.is_pulse:
      self.beat += 1
      self.beat_index = self.beat % BEAT
      self.update_label()
      self.lamp.update_status(self.beat_index)
      self.feedback.weak if self.beat_index else self.feedback.strong

  def did_evaluate_actions(self):
    pass

  def touch_began(self, touch):
    self.is_play = not (self.is_play)
    if self.is_play:
      self.signal.reset()
      self.beat = -1
      self.beat_index = 0

  def did_change_size(self):
    position = self.size / 2
    _w, _h = self.size
    self.label_beat.position = (_w / 2, _h / 1.25)
    self.lamp.change_size_position()
    self.play_botton.change_size_position()


class View(ui.View):

  def __init__(self, scene_node: scene.Node):
    self.bg_color = 0.88
    self.height_ratio: float = 0.96  # todo: safe area

    csnvas_kwargs = {
      'scene': scene_node,
      'frame_interval': frame_interval,
      'shows_fps': shows_fps,
    }
    '''
    self.canvas = scene.SceneView(scene=scene_node,
                                  frame_interval=frame_interval,
                                  shows_fps=shows_fps)
    '''
    self.canvas = scene.SceneView(**csnvas_kwargs)
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

