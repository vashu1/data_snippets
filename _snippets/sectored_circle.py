from common.graphics import *
from PIL import ImageGrab  # pip3 install tk    brew install python-tk
import math
import numpy as np

SIZE = 300
COLORS = ['red', 'green', 'blue'] * 9
win = GraphWin("", SIZE, SIZE, True)


def vector_angle(x, y):  # 0-360
    angle =  np.arctan2(y, x) / np.pi * 180  # +-180 degrees
    return angle if angle > 0 else 360 + angle


def _from_rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % (int(r),int(g),int(b))


for x in range(SIZE):
    for y in range(SIZE):
        xx = SIZE/2 - x
        yy = SIZE/2 - y
        dist = math.sqrt(xx**2 + yy**2)
        if dist < SIZE/2.2:
            angle = vector_angle(xx, yy)
            sector_number = int(len(COLORS) * angle / 360.1)
            # color = COLORS[sector_number]
            if sector_number%3==0:
                color = _from_rgb(0,0,128)
            else:
                c = dist/SIZE*2.2 * 255
                if sector_number%3==1:
                    color = _from_rgb(c,0,0)
                else:
                    color = _from_rgb(0, 255 - c, 0)
            win.create_line(x, y, x + 1, y, fill=color)

win.getMouse()

#cropArea = win.winfo_rootx()+50, win.winfo_rooty()+70, win.winfo_rootx()+win.winfo_width()*2+50, win.winfo_rooty()+win.winfo_height()*2+70
#ImageGrab.grab(cropArea).save('sectored_circle.png')


