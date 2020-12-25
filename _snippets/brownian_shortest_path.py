# create lots of browninan particles, then show path of one that reached the target first
from common.graphics import *
from PIL import ImageGrab
import time
import math
import random

random.seed(7)


win = GraphWin("", 300, 300, True)
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

TARGET_POS = 20
START_POS = 50
PARTICLES_COUNT = 300

class Particle:
    def __init__(self):
        self.saved = []
        self.x = START_POS
        self.y = START_POS
        self.p = None
    
    def step(self):
        self.saved.append((self.x, self.y))
        self.x += random.randint(-3, 3)
        self.y += random.randint(-3, 3)

objs = [Particle() for i in range(PARTICLES_COUNT)]

target = Circle(Point(TARGET_POS, TARGET_POS), 5)
target.setFill('yellow')
target.draw(win)

cropArea = win.winfo_rootx()+50, win.winfo_rooty()+70, win.winfo_rootx()+win.winfo_width()/3*2+50, win.winfo_rooty()+win.winfo_height()/3*2+70

i = 0
while True:
    ImageGrab.grab(cropArea).save('screenshot'+ str(i).zfill(5) +'.png')
    i += 1
    
    for obj in objs:
        obj.step()
        if obj.p:
            obj.p.undraw()
        obj.p = Circle(Point(obj.x, obj.y), 0)
        obj.p.setFill('green')
        obj.p.draw(win)
        
        if math.sqrt((obj.x-TARGET_POS)*(obj.x-TARGET_POS) + (obj.y-TARGET_POS)*(obj.y-TARGET_POS)) <= 5:
            for obj2 in objs:
                obj2.p.undraw()
            ImageGrab.grab(cropArea).save('screenshot'+ str(i).zfill(5) +'.png')
            i += 1
            for s in obj.saved:
                ImageGrab.grab(cropArea).save('screenshot'+ str(i).zfill(5) +'.png')
                i += 1
                
                x, y = s
                p = Circle(Point(x, y), 0)
                p.setFill('red')
                p.draw(win)
            for j in range(5):
                ImageGrab.grab(cropArea).save('screenshot'+ str(i).zfill(5) +'.png')
                i += 1
            time.sleep(5) 
            exit()

#os.system("convert -loop 0 *png animated.gif") # brew install imagemagick
#os.system("rm screenshot*.png")