# covert to greyscale

# param: none

import pathlib 
from pathlib import Path
from PIL import Image

BASE_DIR = pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
img_path = BASE_DIR / "nordic_lights.png"

img =  Image.open(img_path)

# Do a flip of left and right
greyscaledImage = img.convert('L').transpose(Image.FLIP_TOP_BOTTOM)

greyscaledImage.show() # Show the flipped image