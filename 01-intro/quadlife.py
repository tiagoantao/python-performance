from tkinter import ALL, Canvas, Tk

import numpy as np
from PIL import Image, ImageTk

SIZE_X = 200
SIZE_Y = 100

WIN_X = 1000
WIN_Y = 1000
CANVAS_X = 500
CANVAS_Y = 500


def create_pil_image(world):
    pil_img = Image.fromarray(world, mode='P')
    palette = pil_img.getpalette()
    palette[3] = 255
    palette[7] = 255
    palette[11] = 255
    pil_img.putpalette(palette)
    return pil_img


def create_tk_image(canvas, world, pil_img):
    image = ImageTk.PhotoImage(pil_img.resize((CANVAS_X, CANVAS_Y)))
    canvas.create_image(CANVAS_X, CANVAS_Y, image=image)
    canvas.world = world
    canvas.palette = pil_img.getpalette()
    canvas.photo_image = image


def create_start_world(canvas):
    world = np.random.randint(0, 5, (SIZE_Y, SIZE_X), np.uint8)
    pil_img = create_pil_image(world)
    create_tk_image(canvas, world, pil_img)


def get_extended_world(world):
    extended_world = np.empty((SIZE_Y + 2, SIZE_X + 2), np.uint8)   # empty
    extended_world[1:-1, 1:-1] = world  # XXX broadcast

    extended_world[0, 1:-1] = world[-1, :]   # top
    extended_world[-1, 1:-1] = world[0, :]   # bottom
    extended_world[1:-1, 0] = world[:, -1]   # left 
    extended_world[1:-1, -1] = world[:, 0]   # right

    # We do not care about corners
    return extended_world


def live(canvas):
    world = canvas.world
    extended_world = get_extended_world(world)
    new_world = np.empty((SIZE_Y, SIZE_X), np.uint8)
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            states = [0, 0, 0, 0, 0]
            states[extended_world[y, x + 1]] += 1
            states[extended_world[y + 2, x + 1]] += 1
            states[extended_world[y + 1, x]] += 1
            states[extended_world[y + 1, x + 2]] += 1
            alive = states[1:]
            num_alive = sum(alive)
            if num_alive < 2 or num_alive > 3:  # Too few or too many neighbors
                new_world[y, x] = 0
            elif world[y, x] != 0:  # Stays alive
                new_world[y, x] = world[y, x]
            elif num_alive == 3:  # Will be born
                max_represented = max(alive)
                if max_represented > 1:  # majority rule
                    new_world[y, x] = 1 + alive.index(max_represented)
                else:  # diversity - whichever doesn't exist
                    new_world[y, x] = 1 + alive.index(0)
            else:
                new_world[y, x] = 0  # stays dead
    pil_img = create_pil_image(new_world)
    create_tk_image(canvas, new_world, pil_img)
            

root = Tk()
root.geometry(f'{WIN_X}x{WIN_Y}')
canvas = Canvas(root,width=WIN_X,height=WIN_Y)
canvas.pack()
root.bind('<Button-1>', lambda x: live(canvas))

create_start_world(canvas)
root.mainloop()
