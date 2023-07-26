import scene
import ui

frame_interval = 1
shows_fps = True


class Canvas(scene.Scene):

  def setup(self):
    print('setup')
    print(f'{self.size=}')

  def update(self):
    pass
    
  def did_evaluate_actions(self):
    pass

  def did_change_size(self):
    print('did_change_size')
    print(f'{self.size=}')


class View(ui.View):

  def __init__(self, canvas):
    self.bg_color = 1
    self.canvas = canvas
    self.scene_view = scene.SceneView(scene=self.canvas)
    self.scene_view.flex = 'W'
    self.add_subview(self.scene_view)
    
  def layout(self):
    pass


if __name__ == '__main__':
  TITLE = 'title'

  #scene_canvas = SceneCanvas()
  scene_canvas = Canvas()
  view = View(scene_canvas)
  #view = scene.SceneView()
  view.present(style='fullscreen', orientations=['portrait'])

