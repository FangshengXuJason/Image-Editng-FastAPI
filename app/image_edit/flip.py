# reference
# https://pythontic.com/image-processing/pillow/introduction

# param: up_down: bool (choose the direction)

# Flip horizontal and vertical
import pathlib 
from pathlib import Path
from PIL import Image

BASE_DIR = pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
img_path = BASE_DIR / "ingredients-1.png"

img =  Image.open(img_path)

# Do a flip of left and right
flippedImage = img.transpose(Image.FLIP_LEFT_RIGHT)
flippedImage.show() # Show the flipped image

