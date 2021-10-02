#TODO need to fix instability
from graphics import *
from PIL import ImageGrab
from PIL import Image
import time
import math

def grab(bbox=None):
    # http://stackoverflow.com/questions/32799143/imagegrab-python-on-os-x
    f, file = tempfile.mkstemp('.png')
    os.close(f)
    subprocess.call(['screencapture', '-x', file])
    im = Image.open(file)
    im.load()
    os.unlink(file)
    if bbox:
        im = im.crop(bbox)
    return im

tick = 0.01
winWidth = 500
winHeight = 100

win = GraphWin("", winWidth, winHeight, True)

#UNDO
#print "winfo_root", win.winfo_rootx(), win.winfo_rooty()
#print "winfo_width height", win.winfo_width(), win.winfo_height()

cropArea = win.winfo_rootx(), win.winfo_rooty(), win.winfo_rootx()+win.winfo_width(), win.winfo_rooty()+win.winfo_height()

os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

dt = 0.001
STEPS_PER_DRAW = int(1 / dt)
SIZE = 1500
C = 0.1
L = 1

U = [0] * SIZE
I = [0] * (SIZE - 1)

R = 0.001
G = 0.001

t = 0

def lside(t): # input
    return 30 * math.sin(t/30) #-30 #
    #return -30 if ((int(t) % 30) < 15) else +30
    #return 40
    #return 40 if ((t>1) and (t<20)) else 0
    # TODO - sin
    # two pulses of different width
    # meandr?

def step():
    global t, I, U
    nU = [0] * SIZE
    nI = [0] * (SIZE - 1)
    U[0] = lside(t)
    #nope U[SIZE - 1] = 0
    for i in range(SIZE - 2):
        nU[i + 1] = U[i + 1] + (I[i] - I[i + 1]) * C * dt
    for i in range(SIZE - 1):
        nI[i] = I[i] + (U[i] - U[i + 1]) * L * dt
    t = t + dt
    U = nU
    I = nI

def resist():
    global I, U
    for i in range(SIZE - 2):
        U[i + 1] = U[i + 1] * (1 - G)
    for i in range(SIZE - 1):
        I[i] = I[i] * (1 - R)
    
def draw_plot(win):
    win.delete("all") # clear screen
    MIDDLE_Y = winHeight / 2
    win.create_line(0, MIDDLE_Y, winWidth, MIDDLE_Y, fill = "black") # ox
    prevU = None
    prevI = None
    for i in range(winWidth):
        dataIndx = int(i * ((SIZE - 1.0) / winWidth))
        valU = U[dataIndx] + MIDDLE_Y
        if prevU:
            win.create_line(i, prevU, i+1, valU, fill = "blue")
        prevU = valU
        valI = -I[dataIndx] + MIDDLE_Y
        #if prevI:
        #    win.create_line(i, prevI, i+1, valI, fill = "red")
        prevI = valI
    win.redraw()

########  ########  ########  ########  ########

while(t < 2500):
    for i in range(STEPS_PER_DRAW):
        step()
    resist()
    draw_plot(win)
    # ImageGrab.grab(cropArea).save('screenshot'+ str(i) +'.png')
    #time.sleep(tick)

#win.close()

#os.system("convert -loop 0 *png animated.gif")
#os.system("rm screenshot*.png")

