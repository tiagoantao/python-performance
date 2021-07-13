import numpy as np

SIZE_IN_GB = 10

array = np.memmap("data.np", mode="w+",
                  dtype=np.int8, shape=(SIZE_IN_GB * 1024, 1024, 1024))
print(array[-1, -1, :10])

array += 2

array = np.memmap("data.np", mode="r",
                  dtype=np.int8)
print(array.shape)
print(array[:-10])
