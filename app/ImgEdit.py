from email.mime import image
from enum import Enum

class operationName(str, Enum):
    flip = "flip"
    greyscale = "greyscale"
    resize = "resize"
    rotate = "rotate"
    thumbnail = "thumbnail"

from PIL import Image
def flip(original: Image, top_bottem: True) -> Image: 
    if top_bottem: 
        result = original.TRANSPOSE(Image.FLIP_TOP_BOTTOM)
    else: 
        result = original.TRANSPOSE(Image.FLIP_LEFT_RIGHT)
    return result
