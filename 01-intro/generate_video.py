import sys; sys.path.append('.')

import numpy as np

from gui import create_pil_image
from patterns import get_pattern_text, convert_pattern_to_array
from quadlife import live


def create_space_war_world():
    pulsar_pattern_text = get_pattern_text('pulsar')
    pulsar = convert_pattern_to_array(pulsar_pattern_text)
    pulsar_height = pulsar.shape[0]
    pulsar_width = pulsar.shape[1]
    my_world = np.zeros((pulsar_height * 10, pulsar_width * 10), dtype=np.uint8)
    for row in range(10):
        y = row * pulsar_height
        for col in range(10):
            x = col * pulsar_width
            my_world[y:y + pulsar_width, x: x + pulsar_width] = pulsar
    return my_world
    

world = create_space_war_world()
image = create_pil_image(world)
image.save('i.png')
#for i in range(100):
#    print(i)
#    world = quadlife.live(world)
