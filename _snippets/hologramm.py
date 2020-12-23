# generate zone plate
# Printing resolution (dpi) 4800* (horizontal) x 1200 (vertical)
from PIL import Image
RES_Y = 1200
RES_X = 4800
width = 75
img = Image.new('RGB', (RES_X*2, RES_Y*4))
for i in range(RES_Y*2):
    if i % 600 == 0:
        width *= 2
        step = RES_Y / width
        print('step y', step, i)
    if (i % (2*step) != 0):
        img.paste((255,255,255),(0,i,RES_X*2,i+1))

width = 300
for i in range(RES_X*2):
    if i % (600*4) == 0:
        width *= 2
        step = RES_X / width
        print('step x', step, i)
    if (i % (2*step) != 0):
        img.paste((255,255,255),(i,2*RES_Y,i+1,4*RES_Y))

img.save("try.tiff", compression=None, resolution_unit='inch', dpi = (RES_X, RES_Y))
