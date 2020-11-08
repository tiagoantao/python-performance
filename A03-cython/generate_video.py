import sys; sys.path.append('.')

import numpy as np

from gui import create_pil_image
from patterns import get_pattern_text, convert_pattern_to_array
from quadlife import live

SIZE_Y = 250
SIZE_X = 400

def create_space_war_world():
    weekender_pattern_text = get_pattern_text('weekender')
    weekender = convert_pattern_to_array(weekender_pattern_text)
    weekender_height = weekender.shape[0]
    weekender_width = weekender.shape[1]

    pulsar_pattern_text = get_pattern_text('pulsar')
    pulsar = convert_pattern_to_array(pulsar_pattern_text)
    pulsar_height = pulsar.shape[0]
    pulsar_width = pulsar.shape[1]

    my_world = np.zeros((SIZE_Y, SIZE_X), dtype=np.uint8)
    
    for row in range(8):
        y = 100 + row * (5 + weekender_height)
        for col in range(16):
            x = 10 + col * (8 + weekender_width)
            my_world[y:y + weekender_height, x: x + weekender_width] = weekender

    for row in range(3):
        y = 25 + row * (5 + pulsar_height)
        for col in range(22):
            x = 5 + col * (5 + pulsar_width)
            my_world[y:y + pulsar_height, x: x + pulsar_width] = np.where(pulsar==1, 2+row, pulsar)

    return my_world
    

world = create_space_war_world()
image = create_pil_image(world)
image.save(f'frame-0000.png')

for i in range(1, 500):
    print(i)
    world = live(world)
    image = create_pil_image(world)
    image.save(f'frame-{i:04d}.png')
