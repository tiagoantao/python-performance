import sys

import numpy as np
from PIL import Image

image = Image.open("../manning-logo.png").convert("L")
print(image.size)
width, height = image.size
#  https://numpy.org/doc/stable/reference/arrays.interface.html
# print(image.__array_interface__)
image_arr = np.array(image)  # Explain why this works
print(image_arr.shape, image_arr.dtype)    # Shape is flipped of size
print(image_arr.size * image_arr.itemsize, image_arr.nbytes)
print(sys.getsizeof(image_arr))
flipped_from_view = np.flipud(image_arr)
flipped_from_copy = np.flipud(image_arr).copy()
print(image_arr.strides, flipped_from_view.strides)
image_arr[:, :width//2] = 0  # A form of broadcasting?
removed = Image.fromarray(image_arr, "L")
image.save("image.png")
removed.save("removed.png")

flipped_from_view_image = Image.fromarray(flipped_from_view, "L")
flipped_from_view_image.save("flipped_view.png")
flipped_from_copy_image = Image.fromarray(flipped_from_copy, "L")
flipped_from_copy_image.save("flipped_copy.png")


print(image_arr == flipped_from_view.base)
print(np.shares_memory(image_arr, flipped_from_copy),
      np.shares_memory(image_arr, flipped_from_view))


print(flipped_from_copy.base, flipped_from_view.base)
print(flipped_from_view.base is image_arr)
print(flipped_from_view.base == image_arr)



flipped_from_copy = np.flipud(image_arr.copy())

# memoryview - buffer protocol


#FANCY INDEXING
#fancy indexing creates copies


#Cython, check parallel
# https://stackoverflow.com/questions/49803899/passing-returning-cython-memoryviews-vs-numpy-arrays
