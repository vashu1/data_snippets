import math
from PIL import Image

FILE_NAME = "2016_sep.jpg"
W = 0.25 # width of sun-lit side, from 0(nothing) to 1(all disk)

im = Image.open(FILE_NAME)

def v_len(v):
    return math.sqrt(sum([x*x for x in v]))

def get_pixel(x, y):
    x = x % 360
    y = y % 180
    w, h = im.size
    res = 0
    for i in range(int(x / 360.0 * w), int((x + 1) / 360.0 * w)):
        for j in range(int(y / 180.0 * h), int((y + 1) / 180.0 * h)):
            lat = (y - 90) / 180.0 * math.pi
            #print i, j, lat, sum(im.getdata()[y * w + x]) * math.cos(lat)
            res += v_len(im.getdata()[j * w + i]) * math.cos(lat) # sum instead of v_len ?
    return res

def albedo_sum(x, y = 0):
    res = 0
    for i in range(int(- 90 * W), int(+ 90 * W)):
        xi = i + x
        for j in range(-90,90):
            ai = i / 180.0 * math.pi
            aj = j / 180.0 * math.pi
            res += get_pixel(xi, j + y) * math.cos(ai) * math.cos(aj)
    return res

a = []
for i in range(360):
    print i
    a.append(-albedo_sum(i))


w, h = im.size
mi = min(a)
d = h / (max(a) - min(a)) / 2 # 0.0001357343822089434   0.00014
aa = [int((x - mi) * d + h/4) for x in a]

for i in range(w):
    x = int(i * 360 / w)
    if x == 359:
        break
    for j in range(min(aa[x], aa[x+1]), max(aa[x]+1, aa[x+1]+1)):
        im.putpixel((i, j), (255, 0, 0))

im.show()
im.save(FILE_NAME + ".thumbnail.jpg", "JPEG")
