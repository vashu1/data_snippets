# generate animation of elastic merge of bodies
from common.graphics import *
from PIL import ImageGrab
import time
import math
# ImageMagick required  brew install imagemagick

tick = 0.05

winWidth = 500
win = GraphWin("", winWidth, 100, True)

os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')


cropArea = win.winfo_rootx(), win.winfo_rooty(), win.winfo_rootx()+win.winfo_width(), win.winfo_rooty()+win.winfo_height()

lineY = 50

firstPos = 20.0
firstSpeed = 4.0
firstWeight = 100
secondPos = 150.0
secondSpeed = 0.0
secondWeight = 100 # 400
springLen = 30
rigidity = 50 # 3

collided = False

spring = Rectangle(Point(secondPos - springLen, lineY-1), Point(secondPos, lineY+1))
spring.draw(win)
first = Circle(Point(firstPos, lineY), math.sqrt(firstWeight))
first.setFill('green')
first.draw(win)
second = Circle(Point(secondPos, lineY), math.sqrt(secondWeight))
second.setFill('red')
second.draw(win)
	
def drawScene():
	global spring, first, firstPos, second, secondPos
	spring.undraw()
	
	first.move(firstSpeed, 0)
	firstPos += firstSpeed
	second.move(secondSpeed, 0)
	secondPos += secondSpeed
	if collided:
		spring = Rectangle(Point(firstPos, lineY-1), Point(secondPos, lineY+1))
	else:
		spring = Rectangle(Point(secondPos - springLen, lineY-1), Point(secondPos, lineY+1))
	spring.setFill('blue')
	spring.draw(win)

i=10000
while(firstPos<(secondPos - springLen)):
	drawScene()
	#images.append(ImageGrab.grab(cropArea))
	ImageGrab.grab(cropArea).save('screenshot'+ str(i) +'.png')
	i += 1
	time.sleep(tick)

firstPos = secondPos - springLen
collided = True


while(secondPos < winWidth):
	springDelta = springLen - (secondPos - firstPos)
	force = springDelta * rigidity
	firstSpeed -= force / firstWeight
	secondSpeed += force / secondWeight
	
	drawScene()
	#images.append(ImageGrab.grab(cropArea))
	ImageGrab.grab(cropArea).save('screenshot'+ str(i) +'.png')
	i += 1
	time.sleep(tick)
	if i>10160:
		break;
	



#im.save('screenshot.png') # self.__crop = x0, y0, x1, y1
#writeGif('screenshot.gif', images, tick, True, False, 0, False, None)
#convert -delay 10 -loop 0 *png animated.gif    from ImageMagick 

#exit()
os.system("convert -loop 0 *png animated.gif")
os.system("rm screenshot*.png")