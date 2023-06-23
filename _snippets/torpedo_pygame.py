import pygame
import math
import random
import time

FPS = 30

"""
 TODO

"""
RESOLUTION = (600, 600)
SCALE = 3  # 1 pixel == SCALE meters

TORPEDO_COUNT = 20
TORPEDO_SPEED = 25  # 5 ms/ == 10 knots
TORPEDO_INSTABILITY = 3.5
TORPEDO_DROP_TIME = 30

SHIP_LEN = 270
SHIP_SPEED_MS = 15  # 5 ms/ == 10 knots
SHIP_TURN_RATE_DG = 2
print(f'tactical diameter = {round(SHIP_SPEED_MS*(360/SHIP_TURN_RATE_DG)/math.pi)} m')
HITBOX_W = 30

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (43,101,236)

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

    def step(self):
        a = self.direction / 180 * math.pi
        x2 = self.x - math.cos(a) * self.length / 2
        y2 = self.y - math.sin(a) * self.length / 2
        self.wake.add((x2, y2))
        self.wake = set([(x, y) for x, y in self.wake if random.random() > self.wake_decay])
        self.x = self.x + math.cos(a) * self.speed_ms / FPS
        self.y = self.y + math.sin(a) * self.speed_ms / FPS

    def draw(self):
        a = self.direction / 180 * math.pi
        x1 = self.x + math.cos(a) * self.length / 2
        x2 = self.x - math.cos(a) * self.length / 2
        y1 = self.y + math.sin(a) * self.length / 2
        y2 = self.y - math.sin(a) * self.length / 2
        for x, y in self.wake:
            window.set_at((int(x/SCALE), int(y/SCALE)), WHITE)
        pygame.draw.line(window, BLACK, (int(x1 / SCALE), int(y1 / SCALE)), (int(x2 / SCALE), int(y2 / SCALE)), width=3)


ship = Vessel(RESOLUTION[0]/2*SCALE, RESOLUTION[1]*0.75*SCALE, 270, SHIP_LEN, SHIP_SPEED_MS, 0.1 / FPS)

torpedoes = []
for i in range(TORPEDO_COUNT):
    a = random.random() * 2 * math.pi
    d = random.random() * 150
    x = math.cos(a) * d + (1 if i % 2 == 0 else -1) * 200
    y = math.sin(a) * d
    x0 = RESOLUTION[0] / 2 * SCALE
    y0 = RESOLUTION[1] / 2 * SCALE
    t = Vessel(x0 + x, y0 + y, 360 * random.random(), 5, TORPEDO_SPEED, 0.1 / FPS)#0.7 / FPS)
    torpedoes.append(t)

start_time = time.time()
hits = 0

run = True
while run:
    clock.tick(FPS)
    if random.random()<0.01:
        print(f'FPS {round(clock.get_fps(), 1)}')

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

    ship.step()
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

    window.fill(BLUE)
    ship.draw()
    if torpedoes_dropped:
        for t in torpedoes:
            t.draw()
    else:
        for t in torpedoes:
            pygame.draw.circle(window, WHITE, (int(t.x / SCALE), int(t.y / SCALE)), 2)

    msg = f'Torpedo hits: {hits}' if torpedoes_dropped else str(int(TORPEDO_DROP_TIME + start_time - time.time()))
    text_surface = my_font.render(msg, False, (0, 0, 0))
    window.blit(text_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
exit()