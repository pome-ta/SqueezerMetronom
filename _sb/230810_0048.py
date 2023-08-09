import scene
import ui
from objc_util import ObjCClass

import pdbg

UIImageView = ObjCClass('UIImageView')
UIImage = ObjCClass('UIImage')

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True

symbol_play = 'play'
symbol_stop = 'stop'

# xxx: どこまで事前に作るか、いまは無駄に処理してる
play_img_obj = UIImage.systemImageNamed_(symbol_play)
stop_img_obj = UIImage.systemImageNamed_(symbol_stop)

symbol_obj_dic = {
  'play': play_img_obj,
  'stop': stop_img_obj,
}


#@ui.in_background
def get_icon(name: str, size: float) -> ui.Image:
  icon_img = symbol_obj_dic[name]
  image_view_obj = UIImageView.new()
  image_view_obj.setSize_((size, size))
  image_view_obj.setImage_(icon_img)
  image_view_obj.setContentMode_(1)

  image_view = ui.ImageView()
  image_view.width = size
  image_view.height = size
  image_view.objc_instance.addSubview_(image_view_obj)

  outdata = image_view._debug_quicklook_()
  out_png = ui.Image.from_data(outdata, 2)
  #print(out_png)
  return out_png


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.icon_wrap: scene.ShapeNode
    self.icon_sprite: scene.SpriteNode
    self.bbb = get_icon(symbol_play, 49)
    

  def setup(self):
    
    self.__init_guide()
    self.__init_icon()

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    self.guide_change()
    #self.icon_change()

  def __init_icon(self):
    self.icon_wrap = scene.ShapeNode(parent=self,
                                     fill_color='maroon',
                                     stroke_color='clear')
    self.icon_sprite = scene.SpriteNode(parent=self.icon_wrap)
    self.ui_img = get_icon(symbol_play, 256)
    #self.t_img = scene.Texture(self.ui_img)
    self.t_img = scene.Texture(self.bbb)
    self.icon_sprite.texture = self.t_img
    self.icon_change()

  def icon_change(self):
    o_size = min(self.size) / 4
    self.icon_wrap.path = ui.Path.oval(0, 0, o_size, o_size)
    self.icon_wrap.position = self.size / 2
    '''
    self.ui_img = get_icon(symbol_play, o_size)
    self.t_img = scene.Texture(self.ui_img)
    #self.t_img = scene.Texture(self.bbb)
    self.icon_sprite.texture = self.t_img
    '''

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

