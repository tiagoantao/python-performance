import sys

import numpy as np
from PIL import Image

BLOCK_SIZE = 100

fname = sys.argv[1]

schematics = [[-1 if c==' ' else (0 if c == 'O' else 1) for c in line[:-1]] for line in open(fname).readlines()]

world = np.array(schematics)
rows, cols = world.shape


def get_pattern(value):
    if value == -1:
        return np.ones(shape=(BLOCK_SIZE, BLOCK_SIZE), dtype=np.uint8) * 255
    elif value == 1:
        return np.zeros(shape=(BLOCK_SIZE, BLOCK_SIZE), dtype=np.uint8)
    block = np.ones(shape=(BLOCK_SIZE, BLOCK_SIZE), dtype=np.uint8) * 255
    block[0,:] = np.zeros(shape=(BLOCK_SIZE,), dtype=np.uint8)
    block[BLOCK_SIZE-1,:] = np.zeros(shape=(BLOCK_SIZE,), dtype=np.uint8)
    block[:,0] = np.zeros(shape=(1, BLOCK_SIZE), dtype=np.uint8)
    block[:,BLOCK_SIZE-1] = np.zeros(shape=(1, BLOCK_SIZE), dtype=np.uint8)
    return block


image_np = np.empty(shape=(rows * BLOCK_SIZE, cols * BLOCK_SIZE), dtype=np.uint8)
for row in range(rows):
    for col in range(cols):
        pattern = get_pattern(world[row, col])
        image_np[row*BLOCK_SIZE:row*BLOCK_SIZE+BLOCK_SIZE, col*BLOCK_SIZE:col*BLOCK_SIZE+BLOCK_SIZE] = pattern

print(image_np)
image_pil = Image.fromarray(image_np, mode='L')
image_pil.save(f'{fname.split(".")[0]}.png')
