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


def __configuration_by_applying_configuration(
    applys: list) -> UIImageSymbolConfiguration:
  _conf = UIImageSymbolConfiguration.defaultConfiguration()
  for apply in applys:
    _conf = _conf.configurationByApplyingConfiguration_(apply)
  return _conf


def get_symbo_icon(symbol_name: str, point_size: float = 256.0) -> ui.Image:

  size = UIImageSymbolConfiguration.configurationWithPointSize_(point_size)
  color = UIImageSymbolConfiguration.configurationPreferringMonochrome()

  conf = __configuration_by_applying_configuration([size, color])

  # `scene.Texture` で着色するため白色を指定
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

  def __init__(self, bpm: float = 120.0, note: int = 4):
    self.bpm = bpm
    self.note = note  # xxx: 拍数 ?

    self.stock_time: float  # todo: 経過時間加算
    self.past_pulse: int  # todo:
    self.mul_num: float  # todo:
    self.reset()

  def reset(self):
    self.stock_time = 0.0
    self.past_pulse = -1
    

    sec = self.bpm / 60
    step = 4 / self.note  # 拍子対応
    self.mul_num = sec / step

  def increment_time(self, dt: float):
    self.stock_time += dt * self.mul_num

  @property
  def is_pulse(self) -> bool:
    """
    起点として発信(True) する
    note: BPM 起点ではなく、アクションさせたいベース
          8分音符なら8分音符のタイミング(BPM の2倍)
    """

    note_time = int(self.stock_time)
    if note_time != self.past_pulse:
      # xxx: 加算の意味あまりない ? 調整したい
      # xxx: `int` 溢れの可能性ある
      self.past_pulse += 1
      return True
    else:
      return False


class Feedback:

  def __init__(self):
    '''
    https://developer.apple.com/documentation/uikit/uiimpactfeedbackgenerator/feedbackstyle
      
      case light = 0
      case medium = 1
      case heavy = 2
      case soft = 3
      case rigid = 4
    '''
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
    self.icon: scene.SpriteNode

    self.play_texture: scene.Texture
    self.stop_texture: scene.Texture
    self.select_texture: scene.Texture

    self.__set_up()

  def __set_up(self):
    wrap_kwargs = {
      'parent': self,
      'fill_color': 'clear',
      'stroke_color': 'clear',
    }
    self.wrap = scene.ShapeNode(**wrap_kwargs)

    # todo: debug
    self.wrap.stroke_color = 'cyan'

    self.__create_icon()
    self.change_size_position()

  def __create_icon(self):
    play_symbo = get_symbo_icon('play.circle.fill')
    stop_symbo = get_symbo_icon('stop.circle.fill')

    self.play_texture = scene.Texture(play_symbo)
    self.stop_texture = scene.Texture(stop_symbo)
    self.select_texture = None

    self.icon = scene.SpriteNode(parent=self.wrap)
    self.icon.color = TINT_COLOR
    self.up_date(False)

  def up_date(self, is_play):
    self.select_texture = self.stop_texture if is_play else self.play_texture
    self.icon.texture = self.select_texture
    # xxx: 毎回`change` 呼び出しは無駄感
    self.change_size_position()

  def is_touch(self, point) -> bool:
    return self.wrap.frame.contains_point(point)

  def change_size_position(self):
    # 最終的なボタンのサイズを確定
    # xxx: ここでええんか？
    wrap_w = wrap_h = min(self.parent.size) / 4
    pos_x, pos_y = self.parent.size * scene.Size(1 / 2, 1 / 4)

    self.wrap.path = ui.Path.rect(0, 0, wrap_w, wrap_h)
    self.wrap.position = (pos_x, pos_y)

    sq_size = min(self.wrap.size)
    t_w, t_h = self.select_texture.size
    asp = sq_size / max(t_w, t_h)
    self.icon.size = (t_w * asp, t_h * asp)


class Lamp(scene.Node):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.wrap: scene.ShapeNode
    self.dot_matrix: list[list[scene.ShapeNode, ]]

    self.line_width: int = 2

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
    wrap_kwargs = {
      'parent': self,
      'fill_color': 'clear',
      'stroke_color': 'clear',
    }
    self.wrap = scene.ShapeNode(**wrap_kwargs)
    # todo: debug
    #self.wrap.stroke_color = 'cyan'

    _f = self.__create_dot  # xxx: バットマナー!
    self.dot_matrix = [[_f() for _ in range(4)] for _ in range(4)]

    self.change_size_position()
    self.update_status(0)

  def __create_dot(self) -> scene.ShapeNode:
    shape_node = scene.ShapeNode(parent=self.wrap)
    return shape_node

  def update_status(self, active_index: int):
    # todo: 全部書き換えるより、前回のindex と今回のindex のみ処理をする？
    beat_index = active_index // 4 % 4
    note_index = active_index % 4  # 音符
    for yi, rows in enumerate(self.dot_matrix):
      for xi, dot in enumerate(rows):
        if yi == beat_index and xi == note_index:
          dot.fill_color = self.active_is['fill_color']
          dot.stroke_color = self.active_is['stroke_color']
        else:
          dot.fill_color = self.deactive_is['fill_color']
          dot.stroke_color = self.deactive_is['stroke_color']

  def change_size_position(self):
    pos_x, pos_y = self.parent.size * scene.Size(1 / 2, 1 / 1.5)
    wrap_w = min(self.parent.size) / 1.25
    wrap_h = min(self.parent.size) / 1.75

    self.wrap.path = ui.Path.rect(0, 0, wrap_w, wrap_h)
    self.wrap.position = (pos_x, pos_y)

    # 4x4 のdot を囲むpadding 枠
    guide_w = wrap_w / 4
    guide_h = wrap_h / 4

    oval_sq = min(guide_w, guide_h) * 0.64
    oval_path = ui.Path.oval(0, 0, oval_sq, oval_sq)
    oval_path.line_width = self.line_width

    # `wrap` の`position(0, 0)` を左上起点に(あと微調整)
    offset_w = -((wrap_w / 2) - (wrap_w / 8))
    offset_h = +((wrap_h / 2) - (wrap_h / 8))

    for yi, rows in enumerate(self.dot_matrix):
      for xi, dot in enumerate(rows):
        dot.path = oval_path
        x = offset_w + guide_w * xi
        y = offset_h - guide_h * yi
        dot.position = (x, y)


class MetronomScene(scene.Scene):

  def __init__(self, bpm: float = 120.0, note: int = 4, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bpm = bpm
    self.note = note
    self.beat: int = -1
    self.beat_index: int = 0
    self.is_play: bool = False

  def setup(self):
    self.is_play = False
    self.signal = Signal(self.bpm, self.note)
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
      self.lamp.update_status(self.beat)
      self.feedback.weak if self.beat_index else self.feedback.strong

  def did_evaluate_actions(self):
    pass

  def touch_began(self, touch):
    _point = touch.location
    if self.play_botton.is_touch(_point):
      self.is_play = not (self.is_play)
      self.play_botton.up_date(self.is_play)

      if self.is_play:
        self.signal.reset()
        self.beat = -1
        self.beat_index = 0

  def did_change_size(self):
    _w, _h = self.size
    self.label_beat.position = (_w / 2, _h / 2.5)
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
    self.canvas = scene.SceneView(**csnvas_kwargs)

    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  BPM: float = 112.0
  NOTE: int = 16

  metronom_scene = MetronomScene(BPM, NOTE)

  view = View(scene_node=metronom_scene)
  view.present(style='fullscreen', orientations=['portrait'])
  aaa = metronom_scene.lamp.dot_matrix
  #view.present(style='fullscreen')

