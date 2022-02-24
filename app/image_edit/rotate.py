# reference rotate()
# https://pythontic.com/image-processing/pillow/rotate

# param: degree: int(turn the image by this many degrees)

# Rotate +/- n degrees
import pathlib
from PIL import Image

BASE_DIR = pathlib.Path(__file__).parent
img_path = BASE_DIR / "ingredients-1.png"
img = Image.open(img_path)

rotated     = img.rotate(45)# Rotate it by 45 degrees (counter-clockwise)
transposed  = img.transpose(Image.ROTATE_90) # Rotate it by 90 degrees

# img.show() # Display the Original Image
rotated.show() # Display the Image rotated by 45 degrees
transposed.show() # Display the Image rotated by 90 degrees