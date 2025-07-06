import sys
from PIL import Image

#fname = 'death_small.png'
fname = sys.argv[1]
laser_max_msec = 500
step = 0.4
x_mm_start, y_mm_start = 0, 0

img = Image.open(fname)  # Counter({(255, 255, 255): 1065958, (0, 0, 0): 362318, (6, 0, 0): 29

print('''G21         ; Set units to mm
G90         ; Absolute positioning''')

sz = int(200 / step)
img2 = Image.new('RGB', (sz, sz))
min_x, max_x, min_y, max_y = 1e6, 0, 1e6, 0

w, h = img.size
cnt = 0
for y in range(h):  # better to move y rarely
	for x in range(w):
		c = img.getpixel((w - x - 1,y))
		c = c[0] + c[1] + c[2]
		if c == 255 * 3:  # treshold?
			continue
		c = int((3.0 * 255 - c) / (3.0 * 255) * laser_max_msec)
		c = laser_max_msec
		xmm = round(x_mm_start + x * step, 4)
		ymm = round(y_mm_start + y * step, 4)
		print(f'G1 X{xmm} Y{ymm}')
		print('M106')
		print(f'G4 P{c}')
		print('M107 P1')
		cnt += 1
		c2 = int(c / laser_max_msec * 255)
		img2.putpixel((w - x - 1,y), (c2, c2, c2))
		min_x = min(xmm, min_x)
		max_x = max(xmm, max_x)
		min_y = min(ymm, min_y)
		max_y = max(ymm, max_y)

print(f'G1 X{x_mm_start} Y{y_mm_start}')
print('M84         ; Disable motors')
print(f'; Dot count {cnt}', file=sys.stderr)
print(f'; Width {round(max_x - min_x, 1)} mm', file=sys.stderr)
print(f'; Height {round(max_y - min_y, 1)} mm', file=sys.stderr)
print(f'; Time {round(cnt*laser_max_msec/1000*1.1/3600, 1)} h', file=sys.stderr)

with open('hightlight.gcode', 'w') as f:
	impulse = 20
	printf = lambda txt: print(txt, file=f, end='\n')
	printf('G21         ; Set units to mm')
	printf('G90         ; Absolute positioning')
	printf('M106')
	printf(f'G4 P{impulse}')
	printf('M107 P1')
	printf(f'G1 X{max_x} Y{min_y}')
	printf('M106')
	printf(f'G4 P{impulse}')
	printf('M107 P1')
	printf(f'G1 X{max_x} Y{max_y}')
	printf('M106')
	printf(f'G4 P{impulse}')
	printf('M107 P1')
	printf(f'G1 X{min_x} Y{max_y}')
	printf('M106')
	printf(f'G4 P{impulse}')
	printf('M107 P1')
	printf(f'G1 X{min_x} Y{min_y}')
	printf('M106')
	printf(f'G4 P{impulse}')
	printf('M107 P1')
	printf(f'G1 X{min_x} Y{min_y}')

img2.save("res.tiff", compression=None)