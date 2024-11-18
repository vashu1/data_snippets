# brew install ffmpeg
import pygame
import os
import random
from pygame import gfxdraw
import math
import glob
from moviepy.editor import *

pygame.init()

SIZE = (640, 480)
#SIZE = (1920, 1080)
#SIZE = (2560, 1440)

data = [[255]*SIZE[1] for _ in range(SIZE[0])]

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (50, 50)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Spirals')

FPS = 60

clock = pygame.time.Clock()
#print(len(data), len(data[0]))


def check(x, y):  # check if (x, y) inside screen
    if not(0 <= x < SIZE[0]):
        return False
    if not(0 <= y < SIZE[1]):
        return False
    return True

'''
import random
N = 1_000_000
C = 0.5851
s = 0
for i in range(N):
    s += 1
    if random.random() > C:
        s += 1

print(s / (2**0.5) / float(N))
'''

ss0 = 0
ss = 0
def burning(i, j):
    global ss, ss0
    res = []
    for di in [-1, 0, +1]:
        for dj in [-1, 0, +1]:
            if di == 0 and dj == 0:
                continue
            if not check(i + di, j + dj):
                continue
            if data[i+di][j+dj] != 255:
                continue
            f = math.floor(ss) - math.floor(ss0) > 1
            if di * dj != 0 and not f:
                continue
            #if di * dj != 0 and random.random() > (0.2): #not f:#random.random() > (0.2): # < 1/2**0.5: #
            #    continue
            res.append((i+di, j+dj))
    return res


def check_events(events):
    for e in events:
        if e.type == pygame.QUIT:
            quit()

random.seed(6)

def main_window():
    global ss, ss0
    n = 0
    data[200][240] = -255

    while True:
        ss0 = ss
        ss += 2**0.5
        if False and n < 900:
            if n % 10 == 0:
                i = int(SIZE[0] * random.random())
                j = int(SIZE[1] * random.random())
                data[i][j] = -255
        events = pygame.event.get()
        check_events(events)
        pixel_array = pygame.PixelArray(screen)
        burn = []
        for i in range(SIZE[0]):
            for j in range(SIZE[1]):
                v = data[i][j]
                # modify
                if v >= 0:
                    v += 5
                if v > 255:
                    v = 255
                if v < 0:
                    v += 30
                if v < 0:
                    burn += burning(i,j)
                data[i][j] = v
                # show
                if v > 0:
                    pixel_array[i, j] = (0,v,0)
                elif v <= 0:
                    pixel_array[i, j] = (-v,0,0)
        for i, j in burn:
            if data[i][j] > 0:
                data[i][j] = -255
        pixel_array.close()
        pygame.display.update()
        clock.tick(FPS)
        #pygame.image.save(screen, f'screenshot_{n:04}.png')
        n += 1
        #if n > 300:
        #    return
        print(n)


main_window()

# ffmpeg -y -framerate 60 -pattern_type sequence -i screenshot_%04d.png -s:v 1920x1080 -c:v libx264 -pix_fmt yuv420p circle.mp4
# rm screenshot_*.png
#os.system(f'ffmpeg -y -framerate {FPS} -pattern_type sequence -i screenshot_%04d.png -s:v {SIZE[0]}x{SIZE[1]} -c:v libx264 -pix_fmt yuv420p video/circle.mp4')
#_ = [os.remove(png) for png in glob.glob("screenshot_*.png")]

pygame.quit()
