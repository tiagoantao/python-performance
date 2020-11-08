import numpy as np

linear = np.arange(10, dtype=np.uint32)

m2x5 = linear.reshape((2, 5))
print(np.shares_memory(linear, m2x5))
print("2x5", m2x5.shape)
print("2x5 corners", m2x5[0, 0], m2x5[0, 4],
      m2x5[1, 0], m2x5[1, 4])
m5x2 = m2x5.T
print("5x2", m5x2.shape)
print(np.shares_memory(m2x5, m5x2))
print("5x2 corners", m5x2[0, 0], m5x2[0, 1],
      m5x2[4, 0], m5x2[4, 1])

print("linear", linear.shape, linear.strides)
print("5x2 strides", m5x2.strides)
print("2x5 strides", m2x5.strides)
print(m2x5)

# XXX Add rot90

#XXX make contiguous

back = linear[::-1]
print("back", back.shape, back.strides, back[0], back[-1])

linear_step = linear[::2]
print("linear_step", linear_step.shape, linear_step.strides,
      linear_step[0], linear_step[-1])

linear_back_step = linear[::-2]
print("linear_back_step", linear_back_step.shape,
      linear_back_step.strides,
      linear_back_step[0], linear_back_step[-1])

back_m5x2 = m5x2[::-1, ::-1]
print(999, back_m5x2.shape, back_m5x2.strides, back_m5x2[0, 0], back_m5x2[4, 1])


a100 = np.arange(100, dtype=np.uint8).reshape(20, 5)
a100_step_3_2 = a100[::3, ::2]
print(a100_step_3_2.shape, a100_step_3_2.strides)
print(np.shares_memory(a100, a100_step_3_2))
a100_step_3_2_linear = a100_step_3_2.reshape(21)
print(np.shares_memory(a100_step_3_2, a100_step_3_2_linear))
print(a100_step_3_2_linear.shape, a100_step_3_2_linear.strides)

linear.strides = 4,

# sometimes copies are needed
