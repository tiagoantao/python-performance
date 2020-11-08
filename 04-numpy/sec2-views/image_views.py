import numpy as np
from PIL import Image

image = Image.open("../manning-logo.png").convert("L")
width, height = image.size
image_arr = np.array(image)
print("original array", image_arr.shape, image_arr.strides, image_arr.dtype)
image.save("view_initial.png")

invert_rows_arr = image_arr[::-1, :]
print("invert rows", invert_rows_arr.shape, invert_rows_arr.strides,
      np.shares_memory(invert_rows_arr, image_arr))
Image.fromarray(invert_rows_arr).save("invert_x.png")

invert_cols_arr = image_arr[:, ::-1]
print("invert columns", invert_cols_arr.shape, invert_cols_arr.strides,
      np.shares_memory(invert_cols_arr, image_arr))
Image.fromarray(invert_cols_arr).save("invert_y.png")


view_swap_arr = image_arr.reshape(image_arr.shape[1], image_arr.shape[0])
# Same can be done with swapaxes
print("view_swap", view_swap_arr.shape, view_swap_arr.strides,
      np.shares_memory(view_swap_arr, image_arr))
Image.fromarray(view_swap_arr, "L").save("view_swap.png")

trans_arr = image_arr.T
print("transpose", trans_arr.shape, trans_arr.strides,
      np.shares_memory(trans_arr, image_arr))
Image.fromarray(trans_arr, "L").save("transpose.png")

rot_arr = np.rot90(image_arr)
print("rot_arr", rot_arr.shape, rot_arr.strides,
      np.shares_memory(rot_arr, image_arr))
Image.fromarray(rot_arr, "L").save("rot90.png")


slice_arr = image_arr[15:, 77:]
print("slice_arr", slice_arr.shape, slice_arr.strides,
      np.shares_memory(slice_arr, image_arr))
Image.fromarray(slice_arr, "L").save("slice.png")
