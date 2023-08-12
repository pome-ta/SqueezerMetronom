from PIL import Image as ImageP
from io import BytesIO

import scene
import ui
from objc_util import ObjCClass, uiimage_to_png

import pdbg

UIImage = ObjCClass('UIImage')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True

symbol_play = 'play'
symbol_stop = 'stop'

#pdbg.state(UIImageSymbolConfiguration)


class SymbolIcon:

  def __init__(self, name: str, color: str = None, pointsize: float = 256.0):
    uisc = UIImageSymbolConfiguration

    conf: UIImageSymbolConfiguration
    conf = uisc.defaultConfiguration()

    _point_size = uisc.configurationWithPointSize_(pointsize)
    _color = uisc.configurationPreferringMulticolor()

    conf = conf.configurationByApplyingConfiguration_(_point_size)
    conf = conf.configurationByApplyingConfiguration_(_color)

    self.uiimage = UIImage.systemImageNamed_withConfiguration_(name, conf)

  def get_icon_to_size(self, size: float) -> ui.Image:
    width = self.uiimage.size().width
    height = self.uiimage.size().height


def get_symbo_icon(symbol_name: str, point_size: float = 128.0) -> ui.Image:
  conf: UIImageSymbolConfiguration

  conf = UIImageSymbolConfiguration.defaultConfiguration()
  #pdbg.state(conf)
  _point_size = UIImageSymbolConfiguration.configurationWithPointSize_(
    point_size)
  _multicolor = UIImageSymbolConfiguration.configurationPreferringMulticolor()

  conf = conf.configurationByApplyingConfiguration_(_point_size)
  conf = conf.configurationByApplyingConfiguration_(_multicolor)

  ui_image = UIImage.systemImageNamed_withConfiguration_(symbol_name, conf)

  #pdbg.state(ui_image)
  #to_png = uiimage_to_png(ui_image)
  #print(to_png)
  
  #re_img = ui.Image.from_data(to_png)
  #print(re_img)
  newimg = ImageP.new('RGBA', (256,256))
  newimg.

  #iii = ImageP.frombytes('RGBA', (20, 20), to_png)

  #png_img = ui.Image.from_data(iii, 2)
  #png_img = ui.Image.from_data(to_png, 2)
  #return png_img
  '''
  with BytesIO() as bIO:
    iii.save(bIO, 'png')
    re_img = ui.Image.from_data(bIO.getvalue())
    #del iii
    return re_img
  '''


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.icon_wrap: scene.ShapeNode
    self.icon_sprite: scene.SpriteNode
    #self.aaa = get_symbo_icon('cloud.sun.rain.fill')
    '''
    _png_img = get_symbo_icon(symbol_play)
    '''
    _png_img = get_symbo_icon('cloud.sun.rain.fill')
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
    self.icon_sprite.size = (o_size, o_size)

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

