import sys

sys.path.append('.')

SIZE_X = int(sys.argv[1])
SIZE_Y = int(sys.argv[2])
GENERATIONS = int(sys.argv[3])

if len(sys.argv) > 4:
    print('Using standard Python')
    import quadlife
else:
    print('Using Cython')
    import pyximport; pyximport.install()
    import cquadlife as quadlife

world = quadlife.create_random_world(SIZE_Y, SIZE_X)
for i in range(GENERATIONS):
    world = quadlife.live(world)
