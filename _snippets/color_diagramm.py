# draw radial color diagram
from common.graphics import *
import math

import numpy as np

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def _from_rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % (int(r),int(g),int(b)) 

SIZE = 600
BLACK_D = 1#SIZE / 5

win = GraphWin("", SIZE, SIZE, True)

for x in range(0, SIZE):
    for y in range(0, SIZE):
        vx = (x - SIZE/2)
        vy = (y - SIZE/2)
        rho, phi = cart2pol(vx, vy)
        phi = phi / math.pi * 180 + 180
        if rho >= SIZE / 2:
            continue
        if rho < BLACK_D:
            c = rho / BLACK_D * 255
            win.create_line(x, y, x+1, y, fill = _from_rgb(c/3,c/3,c/3))
        else:
            a = int(phi % 120 / 120.0 * 255.0)
            b = 255 - a
            dist = SIZE / 2 - BLACK_D / 2
            ratio = (rho - BLACK_D / 2) / dist
            if ratio < 0:
                continue
            a *= ratio
            b *= ratio
            if phi < 120 or phi == 360:
                r, g, b = a, b, 0
            elif phi < 240:
                r, g, b = b, 0, a
            else:
                r, g, b = 0, a, b
            win.create_line(x, y, x+1, y, fill = _from_rgb(r,g,b))

win.getMouse()
