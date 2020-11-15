import sys

import numpy as np
from PIL import Image

import pyximport; pyximport.install(language_level=3, setup_args={'include_dirs': np.get_include()})
import cyfilter

command = sys.argv[1] if len(sys.argv) > 1 else "python"

image = Image.open("../../04-numpy/aurora.jpg")
gray_filter = Image.open("../filter.png").convert("L")


def python_darken(pixel, dark):
    mean = np.mean(pixel)
    return int(mean * (255 - dark) / 255)


np_darken = np.vectorize(
    python_darken, otypes=[np.uint8],
    signature='(n),()->()')
#    signature='(n,m,z),(n,m)->(n,m)')

image_arr, gray_arr = np.array(image), np.array(gray_filter)
print(image_arr.shape, image_arr.dtype)
print(gray_arr.shape, image_arr.dtype)
if command == "cython_naive":
    darken_arr = cyfilter.darken_naive(image_arr, gray_arr)
elif command == "cython_annotated":
    darken_arr = cyfilter.darken_annotated(image_arr, gray_arr)
else:
    darken_arr = np_darken(image_arr, gray_arr)
print(darken_arr.shape, darken_arr.dtype)
Image.fromarray(darken_arr).save("darken.png")
