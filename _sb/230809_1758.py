import math

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
  return out_png
  
aaa = get_icon(symbol_play, 256)

class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setup(self):
    self.guide = scene.ShapeNode(parent=self,
                                 fill_color='clear',
                                 stroke_color=0.5)

    self.icon = scene.ShapeNode(parent=self,
                                fill_color=0.1,
                                stroke_color='yellow')

    self.wrap_rect = scene.ShapeNode(parent=self,
                                     fill_color='clear',
                                     stroke_color='magenta')
    self.wrap_oval = scene.ShapeNode(parent=self,
                                     fill_color='clear',
                                     stroke_color='cyan')

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    self.guide_change()

    # --- path
    sq_size = min(self.size) / 4
    icon_path = ui.Path()
    for n, i in enumerate(range(0, 360, int(360 / 4))):
      rad = math.radians(i)
      _x = sq_size * math.sin(rad)
      _y = sq_size * math.cos(rad)
      if n == 0:
        icon_path.move_to(_x, _y)
      else:
        icon_path.line_to(_x, _y)
    icon_path.close()

    self.icon.path = icon_path
    # --- icon
    self.icon.position = self.size / 2
    self.icon_frame = self.icon.frame

    # --- wrap
    self.wrap_rect.path = ui.Path.oval(0, 0, *self.icon_frame.size)
    self.wrap_oval.path = ui.Path.rect(0, 0, *self.icon_frame.size)

    self.wrap_rect.position = self.icon_frame.center()
    self.wrap_oval.position = self.icon_frame.center()

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

