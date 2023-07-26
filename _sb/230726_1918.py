import scene
import ui

frame_interval = 1
shows_fps = True


class Canvas(scene.Scene):

  def setup(self):
    self.ground = scene.Node(parent=self)

    self.line = scene.ShapeNode(parent=self.ground)
    self.line.path = self.update_line(128)
    self.line.stroke_color = 'red'
    self.line.position = self.size / 2

    #self.set_line(128)

  def update(self):
    pass

  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    self.line.path = self.update_line(128)
    self.line.position = self.size / 2

  def update_line(self, dire) -> ui.Path:
    w2, h2 = self.size / 2
    path = ui.Path()
    path.move_to(w2 - dire, h2 - dire)
    path.line_to(w2 + dire, h2 + dire)
    return path


class View(ui.View):

  def __init__(self, _canvas):
    self.bg_color = 0.88
    self.height_ratio: float = 0.96  # todo: safe area

    #self.canvas = canvas
    self.canvas = scene.SceneView(scene=_canvas,
                                  frame_interval=frame_interval,
                                  shows_fps=shows_fps)

    #self.scene_view.flex = 'WH'
    self.add_subview(self.canvas)

  def layout(self):
    _, _, w, h = self.frame
    '''
    self.scene_view.width = w
    self.scene_view.height = h * self.height_ratio
    self.scene_view.x = (w / 2) - (self.scene_view.width / 2)
    '''
    self.canvas.frame = (0, 0, w, h * self.height_ratio)


if __name__ == '__main__':
  TITLE = 'title'

  #scene_canvas = SceneCanvas()
  scene_canvas = Canvas()
  view = View(scene_canvas)
  #view = scene.SceneView()
  view.present(style='fullscreen', orientations=['portrait'])

