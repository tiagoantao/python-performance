import numpy as np


def sum_arrays(a, b):  # Assumes both are the same size
    my_sum = np.empty(a.size, dtype=a.dtype)
    for i, (a1, b1) in enumerate(zip(np.nditer(a), np.nditer(b))):
        my_sum[i] = a1 + b1
    return my_sum.reshape(a.shape)


array_100000 = np.arange(100000)
sum_arrays(array_100000, np.ones(array_100000.shape))
array_100000 = np.arange(100000)
array_100000 += array_100000

x = np.array([[0, 20], [250, 500], [1, 2]],
             dtype=np.uint8)
y = np.array([[1, 10], [25, 5]], dtype=np.uint8)

print(sum_arrays(x, y))

a = np.array([0, 20, 21, 9], dtype=np.uint8)
b = np.array([10, 2, 25, 5], dtype=np.uint8)

print(sum_arrays(a, b))

print("add one", a + 1)
print("mutiply by two", a * 2)
print("add a vector", a + [10, 2, 25, 5])
print("multiply by a vector", a * [10, 2, 25, 5])
print("dot (inner) product", a.dot(b))

print("add a vector to itself", x + x)
print("add a vector with column size", x + [1, 2])
# print("add a vector with row size", x + [-1, -2, -3])
print("add a vector with row size", (x.T + [-1, -2, -3]).T)
print("inner product", np.inner(a, b))
print("matrix multiplication", x.dot(y))
# print(x.T.dot(y))

print("matmul ", a @ b)
print("matmul", x @ y)

x[:, 0] = 0
print("assignement broadcasting", x)
