import numpy as np

sizes = [100, 1000, 10000]

# :, 0   / 0, :
# 750 ns / 715 ns
# 1.99 us / 1.5 us
# 4.51 us / 74.9 us
mat = np.random.randint(10, size=(size, size))
mat[:, 0]
mat[0, :]
