from objc_util import ObjCClass
import ui

import pdbg

UIImageView = ObjCClass('UIImageView')
UIImage = ObjCClass('UIImage')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')

play = 'play'
#play = 'battery.0'
ui_image = UIImage.systemImageNamed_(play)

#pdbg.state(ui_image)

#ui_image.size = (48.0, 19.6)

img_w = ui_image.size().width
img_h = ui_image.size().height

s_size = 256.0
i_scale = s_size / max(img_w, img_h)
view_w = img_w * i_scale
view_h = img_h * i_scale

view_s = max(view_w, view_h)

image_view_obj = UIImageView.new()
image_view_obj.setSize_((view_s, view_s))
image_view_obj.setImage_(ui_image)
'''
[UIView.ContentMode | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uiview/contentmode)
case scaleToFill

case scaleAspectFit

case scaleAspectFill

case redraw

case center

case top

case bottom

case left

case right

case topLeft

case topRight

case bottomLeft

case bottomRight

'''
image_view_obj.setContentMode_(1)

#pdbg.state(image_view_obj)

image_view = ui.ImageView()
#image_view.bg_color = 'maroon'
#image_view.width = view_w
#image_view.height = view_h

image_view.width = view_s
image_view.height = view_s

image_view.objc_instance.addSubview_(image_view_obj)

outdata = image_view._debug_quicklook_()
out_png = ui.Image.from_data(outdata, 2)
out_view = ui.ImageView(image=out_png)
out_view.bg_color = 'cyan'

#pdbg.state(ui_image)

