import scene
import ui

frame_interval = 4
shows_fps = True


class Canvas(scene.Scene):

  #@ui.in_background
  def set_check_fps(self):
    print(self.frame_interval)
  
  def setup(self):
    self.fps_over = False
    self.st_dt = self.view.frame_interval / 60
    self.base_bg = self.background_color
    self.error_bg = 'maroon'
    
    self.ground = scene.Node(parent=self)

    self.line = scene.ShapeNode(parent=self.ground)
    self.line.path = self.update_line(128)
    self.line.stroke_color = 'red'
    self.line.position = self.size / 2
    #self.set_check_fps()

    #self.set_line(128)

  def update(self):
    pass

  def did_evaluate_actions(self):
    #self.set_check_fps()
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

  def __init__(self, scene_node:scene.Node):
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

  canvas = Canvas()
  view = View(scene_node=canvas)
  view.present(style='fullscreen', orientations=['portrait'])

