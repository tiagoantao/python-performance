import pyximport
import line_profiler

import numpy as np
from PIL import Image

pyximport.install(
    language_level=3,
    setup_args={
        'options': {"build_ext": {"define": 'CYTHON_TRACE'}},
        'include_dirs': np.get_include()})

import cyfilter_mv as cyfilter

image = Image.open("../../04-numpy/aurora.jpg")
gray_filter = Image.open("../filter.png").convert("L")
image_arr, gray_arr = np.array(image), np.array(gray_filter)

profile = line_profiler.LineProfiler(cyfilter.darken_annotated)
darken_arr = profile.runcall(cyfilter.darken_annotated, image_arr, gray_arr)
profile.print_stats()

Image.fromarray(darken_arr).save("darken.png")
