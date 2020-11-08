import sys
import timeit

import numpy as np

for size in [1, 10, 100, 1000, 10000, 100000, 200000, 400000, 800000, 1000000]:
    print(size, end=",")
    my_array = np.arange(size, dtype=np.uint16)
    #print(sys.getsizeof(my_array))
    print(my_array.data.nbytes, end=",")
    view_time = timeit.timeit(
        "my_array.view()",
        f"import numpy; my_array = numpy.arange({size})")
    print(view_time, end=",")
    copy_time = timeit.timeit(
        "my_array.copy()",
        f"import numpy; my_array = numpy.arange({size})")
    print(copy_time)
    copy_gc_time = timeit.timeit(
        "my_array.copy()",
        f"import numpy; import gc; gc.enable(); my_array = numpy.arange({size})")
    #print(copy_gc_time)

    #print()
