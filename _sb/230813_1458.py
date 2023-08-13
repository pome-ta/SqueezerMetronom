import scene
import ui
from objc_util import ObjCClass, uiimage_to_png

import pdbg

UIImage = ObjCClass('UIImage')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')


def configuration_by_applying_configuration(
    applys: list) -> UIImageSymbolConfiguration:
  _conf = UIImageSymbolConfiguration.defaultConfiguration()
  for apply in applys:
    _conf = _conf.configurationByApplyingConfiguration_(apply)
  return _conf


symbol_icon = 'cloud.sun.rain.fill'

pointsize = 256.0
_point_size = UIImageSymbolConfiguration.configurationWithPointSize_(pointsize)

_color = UIImageSymbolConfiguration.configurationPreferringMulticolor()

conf = configuration_by_applying_configuration([_point_size, _color])

uiimage = UIImage.systemImageNamed_withConfiguration_(symbol_icon, conf)

png_bytes = uiimage_to_png(uiimage)

img_png = ui.Image.from_data(png_bytes, 2)

teximg = scene.Texture(img_png)
spnode = scene.SpriteNode()
spnode.texture = teximg
spnode.size = (100, 100)

