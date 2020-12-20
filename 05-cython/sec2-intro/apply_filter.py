import sys

import numpy as np
from PIL import Image

import pyximport; pyximport.install(
    language_level=3,
    setup_args={
        'options': {'define_macrsdcsdos': {"CYTHON_TRACE": "1"}},
        'include_dirs': np.get_include()})
import cyfilter

command = sys.argv[1] if len(sys.argv) > 1 else "python"

image = Image.open("../../04-numpy/aurora.jpg")
gray_filter = Image.open("../filter.png").convert("L")


def python_darken(image, darken_filter):
    nrows, ncols, _rgb_3 = image.shape
    dark_image = np.empty(shape=(nrows, ncols), dtype=np.uint8)
    for row in range(nrows):
        for col in range(ncols):
            pixel = image[row, col]
            mean = np.mean(pixel)
            dark_pixel = darken_filter[row, col]
            dark_image[row, col] = mean * (255 - dark_pixel) // 255
    return dark_image


def python_darken_ufunc(pixel, dark):
    mean = np.mean(pixel)
    return int(mean * (255 - dark) / 255)


np_darken = np.vectorize(
    python_darken_ufunc, otypes=[np.uint8],
    signature='(n),()->()')
#    signature='(n,m,z),(n,m)->(n,m)')


def dark_annotated():
    darken_arr = cyfilter.darken_annotated(image_arr, gray_arr)
    return darken_arr


image_arr, gray_arr = np.array(image), np.array(gray_filter)
print(image_arr.shape, image_arr.dtype)
print(gray_arr.shape, image_arr.dtype)
if command == "cython_naive":
    darken_arr = cyfilter.darken_naive(image_arr, gray_arr)
elif command == "cython_annotated":
    darken_arr = dark_annotated()
elif command == "python_vector":
    darken_arr = np_darken(image_arr, gray_arr)
else:
    darken_arr = python_darken(image_arr, gray_arr)
print(darken_arr.shape, darken_arr.dtype)
Image.fromarray(darken_arr).save("darken.png")
