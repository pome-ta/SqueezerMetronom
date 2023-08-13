import scene
import ui
from objc_util import ObjCClass, uiimage_to_png

import pdbg

UIImage = ObjCClass('UIImage')
UIColor = ObjCClass('UIColor')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True

symbol_play = 'play.fill'
symbol_stop = 'stop'


def configuration_by_applying_configuration(
    applys: list) -> UIImageSymbolConfiguration:
  _conf = UIImageSymbolConfiguration.defaultConfiguration()
  for apply in applys:
    _conf = _conf.configurationByApplyingConfiguration_(apply)
  return _conf


def get_symbo_icon(symbol_name: str, point_size: float = 128.0) -> ui.Image:

  size = UIImageSymbolConfiguration.configurationWithPointSize_(point_size)
  #color = UIImageSymbolConfiguration.configurationPreferringMulticolor()
  color = UIImageSymbolConfiguration.configurationPreferringMonochrome()

  conf = configuration_by_applying_configuration([size, color])
  #conf = configuration_by_applying_configuration([size])

  tint_color = UIColor.systemDarkGrayColor()
  tint_color = UIColor.tintColor()
  
  '''
  case automatic = 0
  case alwaysOriginal = 1
  case alwaysTemplate = 2
  '''

  ui_image = UIImage.systemImageNamed_withConfiguration_(
    symbol_name, conf).imageWithTintColor_renderingMode_(tint_color, 1)
  #imageWithTintColor_renderingMode_
  
  #pdbg.state(UIColor)
  pdbg.state(ui_image)
  #ui_image.imageWithTintColor_renderingMode_(UIColor.systemDarkGrayColor(), 1)

  #pdbg.state(ui_image)
  #pdbg.state(UIColor.systemDarkGrayColor())

  png_bytes = uiimage_to_png(ui_image)
  png_img = ui.Image.from_data(png_bytes, 2)
  return png_img


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.icon_wrap: scene.ShapeNode
    self.icon_sprite: scene.SpriteNode

    _png_img = get_symbo_icon(symbol_play)

    #_png_img = get_symbo_icon('cloud.sun.rain.fill')
    self.play_tex = scene.Texture(_png_img)

  def setup(self):
    self.__init_guide()
    self.__init_icon()

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    self.guide_change()
    self.icon_change()

  def __init_icon(self):
    self.icon_wrap = scene.ShapeNode(parent=self,
                                     fill_color='maroon',
                                     stroke_color='clear')
    self.icon_sprite = scene.SpriteNode(parent=self.icon_wrap)
    self.icon_change()

  def icon_change(self):
    o_size = min(self.size) / 4
    self.icon_wrap.path = ui.Path.oval(0, 0, o_size, o_size)
    self.icon_wrap.position = self.size / 2

    self.icon_sprite.texture = self.play_tex
    self.icon_sprite.size = (o_size * 0.64, o_size * 0.64)
    #self.icon_sprite.color = 'cyan'

  def __init_guide(self):
    self.guide = scene.ShapeNode(parent=self,
                                 fill_color='clear',
                                 stroke_color=0.5)
    self.guide_change()

  def guide_change(self):
    guide_path = ui.Path()

    guide_path.move_to(0, 0)
    guide_path.line_to(self.size.x, self.size.y)
    guide_path.move_to(self.size.x, 0)
    guide_path.line_to(0, self.size.y)

    guide_path.move_to(self.size.x / 2, 0)
    guide_path.line_to(self.size.x / 2, self.size.y)
    guide_path.move_to(0, self.size.y / 2)
    guide_path.line_to(self.size.x, self.size.y / 2)
    self.guide.path = guide_path
    self.guide.position = self.size / 2


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

