import math

import scene
import ui

from objc_util import ObjCClass

BEAT: int = 4

frame_interval: int = 1
shows_fps: bool = True


class Canvas(scene.Scene):

  def __init__(self, bpm: float, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setup(self):
    self.guide = scene.ShapeNode(parent=self,
                                 fill_color='clear',
                                 stroke_color=0.5)

    self.icon = scene.ShapeNode(parent=self)
    self.wrap = scene.ShapeNode(parent=self,
                                fill_color='clear',
                                stroke_color='maroon')

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    self.guide_change()
    self.icon.position = self.size / 2

    self.icon_frame = self.icon.frame
    self.wrap.path = ui.Path.rect(0, 0, *self.icon_frame.size)

    self.wrap.position = self.icon_frame.center()

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

