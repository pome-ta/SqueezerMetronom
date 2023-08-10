import scene
import ui
from objc_util import ObjCClass, on_main_thread

import pdbg

UIImageView = ObjCClass('UIImageView')
UIImage = ObjCClass('UIImage')

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True

symbol_play = 'play'
symbol_stop = 'stop'


class SymbolIcon:

  def __init__(self, name: str):
    self.uiimage = UIImage.systemImageNamed_(name)
    self.obj_img_view = UIImageView.new()
    self.obj_img_view.setImage_(self.uiimage)
    self.obj_img_view.setContentMode_(1)

    self.ui_img_view = ui.ImageView()
    self.ui_img_view.objc_instance.addSubview_(self.obj_img_view)

  @on_main_thread
  def get_image(self, square_size: float) -> ui.Image:
    self.obj_img_view.setSize_((square_size, square_size))
    self.ui_img_view.width = square_size
    self.ui_img_view.height = square_size
    
    '''
    with ui.ImageContext(square_size, square_size, 2)as ctx:
      self.ui_img_view.draw_snapshot()
      self.out_img = ctx.get_image()
      return self.out_img
    
    '''
    #pdbg.state(self.ui_img_view.objc_instance.image())
    self.out_data = self.ui_img_view._debug_quicklook_()
    self.out_img = ui.Image.from_data(self.out_data, 2)
    return self.out_img


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.icon_wrap: scene.ShapeNode
    self.icon_sprite: scene.SpriteNode
    self.play_symbol = SymbolIcon(symbol_play)

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
    
    self.play_img = self.play_symbol.get_image(o_size * 0.88)
    self.play_tex = scene.Texture(self.play_img)
    self.icon_sprite.texture = self.play_tex

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

