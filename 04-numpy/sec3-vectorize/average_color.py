import numpy as np
from PIL import Image

image = Image.open("../manning-logo.png").convert("L")
width, height = image.size
image_arr = np.array(image)


def get_average_color_or_red(row):
    if np.all(row == row[0]):
        return np.array([255, 0, 0], dtype=np.uint8)
    mean = np.mean(row)
    return np.array([mean, mean, mean], dtype=np.uint8)


vec_get_average_color_or_red = np.vectorize(
    get_average_color_or_red, otypes=[np.uint8],
    signature="(n)->(m)")

row_average_arr = vec_get_average_color_or_red(image_arr)
col_average_arr = vec_get_average_color_or_red(image_arr.T)

print(row_average_arr.max(), row_average_arr.dtype, row_average_arr.shape)
Image.fromarray(np.expand_dims(row_average_arr, axis=0)).save("row_color.png")

print(col_average_arr.max(), col_average_arr.dtype, col_average_arr.shape)
Image.fromarray(np.expand_dims(brighter_1d_arr, axis=0)).save("col_color.png")

