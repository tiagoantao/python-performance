import numpy as np
from PIL import Image

image = Image.open("../aurora.jpg")
width, height = image.size
image_arr = np.array(image)
print(image_arr.shape, image_arr.dtype)

def get_grayscale_color(row):
    mean = np.mean(row)
    return int(mean)


vec_get_grayscale_color = np.vectorize(
    get_grayscale_color, otypes=[np.uint8],
    signature="(n)->()")

grayscale_arr = vec_get_grayscale_color(image_arr)
#grayscale_arr = np.mean(image_arr, axis=2).astype(np.uint8)

print(grayscale_arr.max(), grayscale_arr.dtype, grayscale_arr.shape)
Image.fromarray(grayscale_arr).save("grayscale.png")


