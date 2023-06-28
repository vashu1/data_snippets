import pygame  # python3 -m pip install pygame
from PIL import Image  # python3 -m pip install pillow
import math
import random
import time
import os
import glob

FPS = 30  # frames per second

RESOLUTION = (1200, 800)  # screen width / height in pixels
SCALE = 3  # 1 pixel == SCALE meters
TIME_SCALE = 5  # speed up simulation

TORPEDO_COUNT = 20  # how many torpedoes dropped
TORPEDO_SPEED = 45 * 0.5 * TIME_SCALE  # 5 ms/ == 10 knots
TORPEDO_INSTABILITY = 3.5  # every meter torpedo changes direction at random_uniform(TORPEDO_INSTABILITY/2)
TORPEDO_DROP_TIME = 45 / TIME_SCALE # how many seconds torpedoes fall
WAKE_DECAY_TORPEDO = 0.1 / FPS * TIME_SCALE  # decrease it to lengthen wake

SHIP_LEN = 270  # meters
SHIP_SPEED_MS = 15 * TIME_SCALE  # 5 ms/ == 10 knots
SHIP_TURN_RATE_DG = 2 * TIME_SCALE  # left/right full rudder turn rate in degrees per second
WAKE_DECAY_SHIP = 0.1 / 4 / FPS * TIME_SCALE  # decrease it to lengthen wake
print(f'tactical diameter = {round(SHIP_SPEED_MS*(360/SHIP_TURN_RATE_DG)/math.pi)} m')
HITBOX_W = 30  # width of the ship in meters

WHITE = (255,255,255)  # wake color / torpedo drop points
BLACK = (0,0,0)  # ship/torpedo body
BLUE = (43,101,236)  # ocean color

# clean screenshots
_ = [os.remove(png) for png in glob.glob("screenshot_torpedo_*.png")]
_ = [os.remove(png) for png in glob.glob("torpedo_animated.gif")]

pygame.init()
window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


class Vessel():
    def __init__(self, x, y, direction, length, speed_ms, wake_decay):
        self.speed_ms = float(speed_ms)
        self.direction = float(direction)
        self.x = float(x)
        self.y = float(y)
        self.length = float(length)
        self.wake_decay = float(wake_decay)
        self.wake = set([])

    """ change vessel position, save new wake point, decay old wake points """
    def step(self):
        a = self.direction / 180 * math.pi
        x2 = self.x - math.cos(a) * self.length / 2
        y2 = self.y - math.sin(a) * self.length / 2
        neighbours = set([(x2 + dx, y2 + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]])
        self.wake.add((x2, y2))
        # decay old points
        self.wake = set([(x, y) for x, y in self.wake if random.random() > self.wake_decay])
        self.x = self.x + math.cos(a) * self.speed_ms / FPS
        self.y = self.y + math.sin(a) * self.speed_ms / FPS

    # draw vessel and it's wake
    def draw(self):
        a = self.direction / 180 * math.pi
        x1 = self.x + math.cos(a) * self.length / 2
        x2 = self.x - math.cos(a) * self.length / 2
        y1 = self.y + math.sin(a) * self.length / 2
        y2 = self.y - math.sin(a) * self.length / 2
        for x, y in self.wake:
            window.set_at((int(x/SCALE), int(y/SCALE)), WHITE)
        pygame.draw.line(window, BLACK, (int(x1 / SCALE), int(y1 / SCALE)), (int(x2 / SCALE), int(y2 / SCALE)), width=3)


# ship starting position
ship = Vessel(RESOLUTION[0]/2*SCALE, RESOLUTION[1]/2*SCALE + 750, 270, SHIP_LEN, SHIP_SPEED_MS, WAKE_DECAY_SHIP)
# uncomment ship2 lines to add ghost ship (does not take torpedo hits) that goes straight
#ship2 = Vessel(RESOLUTION[0]/2*SCALE, RESOLUTION[1]/2*SCALE + 750, 270, SHIP_LEN, SHIP_SPEED_MS, WAKE_DECAY_SHIP)

# torpedoes drop points
torpedoes = []
for i in range(TORPEDO_COUNT):
    dot = (0,750)
    dst = 750
    a2 = -(i/(TORPEDO_COUNT-1) * 50 + 25) / 180 * math.pi
    if i % 2 == 0:
        a2 = math.pi - a2
    a = random.random() * 2 * math.pi
    d = random.random()**0.5 * 200
    x = math.cos(a) * d + dot[0] + math.cos(a2) * dst * 1
    y = math.sin(a) * d + dot[1] + math.sin(a2) * dst * 1.5
    x0 = RESOLUTION[0] / 2 * SCALE
    y0 = RESOLUTION[1] / 2 * SCALE

    t = Vessel(x0 + x, y0 + y, 180 * random.random(), 5, TORPEDO_SPEED, WAKE_DECAY_TORPEDO)
    torpedoes.append(t)

start_time = time.time()
hits = 0
n = 0

run = True
while run:
    n += 1
    if n % (FPS / TIME_SCALE) == 0:
        pygame.image.save(window, f'screenshot_torpedo_{n:03}.png')
    clock.tick(FPS)
    if random.random() < 0.1 / FPS:
        print(f'real FPS {round(clock.get_fps(), 1)}')

    # are torpedoes in the water?
    torpedoes_dropped = (time.time() - start_time) > TORPEDO_DROP_TIME

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.direction -= SHIP_TURN_RATE_DG / FPS
    if keys[pygame.K_RIGHT]:
        ship.direction += SHIP_TURN_RATE_DG / FPS
    if keys[pygame.K_ESCAPE]:
        run = False

    # move ship and torpedoes
    ship.step()
    #ship2.step()
    if torpedoes_dropped:
        new_torpedoes = []
        for t in torpedoes:
            t.direction += (random.random() - 0.5) * TORPEDO_INSTABILITY / math.sqrt(TORPEDO_SPEED / FPS)
            #if random.random() < 0.15 / FPS:
            #    t.direction = 360 * random.random()
            t.step()
            x_ = t.x - ship.x
            y_ = t.y - ship.y
            a = ship.direction / 180 * math.pi
            x = math.cos(a) * x_ + math.sin(a) * y_
            y = - math.sin(a) * x_ + math.cos(a) * y_
            if abs(x) < SHIP_LEN / 2 and abs(y) < HITBOX_W / 2:
                hits += 1
            else:
                new_torpedoes.append(t)
        torpedoes = new_torpedoes

    # draw everything
    window.fill(BLUE)
    ship.draw()
    #ship2.draw()
    if torpedoes_dropped:
        for t in torpedoes:
            t.draw()
    else:
        for t in torpedoes:
            pygame.draw.circle(window, WHITE, (int(t.x / SCALE), int(t.y / SCALE)), 2)

    msg = f'Torpedo hits: {hits}' if torpedoes_dropped else str(int(TIME_SCALE*(TORPEDO_DROP_TIME + start_time - time.time())))
    text_surface = my_font.render(msg, False, (0, 0, 0))
    window.blit(text_surface, (10, 10))

    pygame.display.flip()

# create GIF
imgs = glob.glob("screenshot_torpedo_*.png")
imgs.sort()
print('\n'.join(imgs))
frames = []
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

frames[0].save('torpedo_animated.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=200, loop=1000)

pygame.quit()
exit()