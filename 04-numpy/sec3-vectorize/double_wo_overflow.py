import numpy as np
from PIL import Image

image = Image.open("../manning-logo.png").convert("L")
width, height = image.size
image_arr = np.array(image)


def double_wo_overflow(v):
    return min(2 * v, 255)

vec_double_wo_overflow = np.vectorize(
    double_wo_overflow, otypes=[np.uint8])

brighter_arr = vec_double_wo_overflow(image_arr)
print(brighter_arr.max(), brighter_arr.dtype)
Image.fromarray(brighter_arr).save("vec_brighter.png")


def double_wo_overflow_1d(row):
    return np.minimum(
        np.multiply(2, row,
                    dtype=np.uint16), 255)


vec_double_wo_overflow_1d = np.vectorize(
    double_wo_overflow_1d, otypes=[np.uint8],
    signature="(n)->(n)")

brighter_1d_arr = vec_double_wo_overflow_1d(image_arr)
print(brighter_1d_arr.max(), brighter_1d_arr.dtype, brighter_1d_arr.shape)
Image.fromarray(brighter_1d_arr).save("vec_brighter_1d.png")

def double_wo_overflow_horrible(row):
    new_row = row.copy()
    for i, v in enumerate(new_row):
        v2 = 2 * v
        if v2 > 255:
            v2 = 255
    return new_row


vec_double_wo_overflow_horrible = np.vectorize(
    double_wo_overflow_horrible,
    signature="(n)->(n)")


brighter_horrible_arr = vec_double_wo_overflow_horrible(image_arr)
print(brighter_horrible_arr.max(), brighter_horrible_arr.dtype, brighter_horrible_arr.shape)
