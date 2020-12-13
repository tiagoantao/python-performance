import cProfile
import pstats
import pyximport

import numpy as np
from PIL import Image

pyximport.install(
    setup_args={
        'include_dirs': np.get_include()})

import cyfilter_prof as cyfilter

image = Image.open("../../04-numpy/aurora.jpg")
gray_filter = Image.open("../filter.png").convert("L")
image_arr, gray_arr = np.array(image), np.array(gray_filter)

# We just want to profile this
cProfile.run("cyfilter.darken_annotated(image_arr, gray_arr)", "apply_filter.prof")
s = pstats.Stats("apply_filter.prof")
s.strip_dirs().sort_stats("time").print_stats()
