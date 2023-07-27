import scene
import ui

BEAT: int = 4
frame_interval: int = 1
shows_fps: bool = True


class Canvas(scene.Scene):

  def __init__(self, bpm: float):
    super().__init__()
    self.bpm = bpm
    self.stack_time: float = 0.0

  def setup(self):
    self.ground = scene.Node(parent=self)

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    pass


class View(ui.View):

  def __init__(self, scene_node: scene.Node):
    self.bg_color = 0.88
    self.height_ratio: float = 0.96  # todo: safe area

    self.canvas = scene.SceneView()
    self.canvas.scene = scene_node
    self.canvas.frame_interval = frame_interval
    self.canvas.shows_fps = shows_fps

    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  TITLE = 'title'
  BPM: float = 120.0

  canvas = Canvas(BPM)
  view = View(scene_node=canvas)
  view.present(style='fullscreen', orientations=['portrait'])

