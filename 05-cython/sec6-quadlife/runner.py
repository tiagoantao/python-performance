import sys

sys.path.append('.')
import quadlife

SIZE_Y = 150
SIZE_X = 200

world = quadlife.create_random_world(SIZE_Y, SIZE_X)
for i in range(100):
    print(i)
    world = quadlife.live(world)
