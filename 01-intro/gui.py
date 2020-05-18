import sys
from tkinter import ALL, Canvas, Tk

from PIL import Image, ImageTk

sys.path.append('.')
import quadlife

SIZE_Y = 100
SIZE_X = 200

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
    palette[12] = 255
    palette[14] = 255
    pil_img.putpalette(palette)
    return pil_img


def create_tk_image(canvas, world, pil_img):
    image = ImageTk.PhotoImage(pil_img.resize((CANVAS_X, CANVAS_Y)))
    canvas.create_image(CANVAS_X, CANVAS_Y, image=image)
    canvas.world = world
    canvas.palette = pil_img.getpalette()
    canvas.photo_image = image


def live_on_gui(canvas):
    old_world = canvas.world
    new_world = quadlife.live(old_world)
    pil_img = create_pil_image(new_world)
    create_tk_image(canvas, new_world, pil_img)
            

root = Tk()
root.geometry(f'{WIN_X}x{WIN_Y}')
canvas = Canvas(root,width=WIN_X,height=WIN_Y)
canvas.pack()
root.bind('<Button-1>', lambda _: live_on_gui(canvas))

world = quadlife.create_random_world(SIZE_Y, SIZE_X)
pil_img = create_pil_image(world)
create_tk_image(canvas, world, pil_img)
root.mainloop()
