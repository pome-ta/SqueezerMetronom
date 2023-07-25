import scene
import ui

frame_interval = 1
shows_fps = True

'''
class SceneCanvas(scene.SceneView):

  def __init__(self):
    pass
'''

class View(ui.View):

  def __init__(self, canvas):
    self.bg_color = 1
    self.canvas = canvas
    self.add_subview(self.canvas)


if __name__ == '__main__':
  TITLE = 'title'

  #scene_canvas = SceneCanvas()
  scene_canvas = scene.SceneView()
  view = View(scene_canvas)
  #view = scene.SceneView()
  view.present(style='fullscreen', orientations=['portrait'])

