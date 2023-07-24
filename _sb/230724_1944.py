import scene
import ui


class View(ui.View):

  def __init__(self, *args, **kwargs):
    # --- 変数反映
    self.bg_color = 1

  def layout(self):
    _, _, w, h = self.frame


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

