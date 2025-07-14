'''

!!!

In LaserWeb, the "cut rate" refers to the feed rate, which is the speed at which the laser head
moves across the material during cutting, typically measured in millimeters per minute (mm/min)

50 mm/s * 60 s/min = 3000 mm/min

Trim Pixels will remove all trailing white pixels from the both ends of each line. This can significantly reduce the time to engrave and the g-code file size.

Join Pixels
Draw a single line if several consecutive pixels of the same intensity are detected.

Burn White
Avoids turning off the laser power but prevents burning by forcing the S value to zero. 
https://laserweb.yurl.ch/documentation/cam-operations/40-laser-operations/8-laser-raster-settings

'''
import sys
from PIL import Image

fname = 'death.gcode'
#fname = sys.argv[1]
laser_max_msec = 50
step = 0.2

'''
; First Move
G0 X82.55 Y2.43 

G0 X82.55 Y2.43 S0.0000
G1 X82.65 S0.3373
X83.65 S0.6863
X83.75 S0.0275
G0 X84.15 Y2.63 S0.0000
G1 X84.05 S0.1725
X83.85 S0.6157
X83.65 S0.9333
X82.65 S1.0000
X82.45 S0.9647

->

M106  ; Set Fan Speed
G4 P47 ; Dwell
M107 P1  ; Fan Off
G0 Y0.2 X65
M106

% cat death.gcode| grep Y | grep -v "S0.0000"
G0 X82.55 Y2.43 

% grep Y death.gcode| grep -v G0 | wc -l 
       0
'''


def parse_part(cmd_part):
	return float(cmd_part[1:])


def parse(line):
	line = line.split(' ')
	cmd = None
	if line[0].startswith('G'):
		cmd = line[0]
		line = line[1:]
	x, y, s = None, None, None
	for i in line:
		if i == ';':
			break
		if i.startswith('X'):
			x = parse_part(i)
		if i.startswith('Y'):
			y = parse_part(i)
		if i.startswith('S'):
			s = parse_part(i)
	return cmd, x, y, s


with open(fname) as f:
	lines = f.readlines()

sz = int(200*10 * 0.1 / step)
img = Image.new('RGB', (sz, sz))
min_x, max_x, min_y, max_y = 1e6, 0, 1e6, 0
prev_x, prev_y, prev_x_old, prev_y_old = None, None, None, None
with open('result.gcode', 'wt') as f:
	for indx, line in enumerate(lines):
		#print(line)
		line = line.strip()
		if indx and lines[indx-1].startswith('; stripped:'):
			line += lines[indx-1].split('; stripped:')[1]
		if not line or line.startswith(';') or not (' S0' in line or ' S1' in line):
			_ = f.write(f'{line}\n')
			if line.startswith('G0'):
				_, prev_x_old, prev_y_old, _ = parse(line)
		else:
			cmd, x, y, s = parse(line)
			if prev_x_old:
				prev_x = prev_x_old
			if prev_y_old:
				prev_y = prev_y_old
			prev_x_old, prev_y_old = x, y
			#if y and y>50:
			#	break
			if x is not None:
				min_x = min(x, min_x)
				max_x = max(x, max_x)
			if y is not None:
				min_y = min(y, min_y)
				max_y = max(y, max_y)
			if y is not None:
				assert cmd is not None
				if x is None:
					_ = f.write(f'{cmd} Y{y}\n')
				else:
					_ = f.write(f'{cmd} X{x} Y{y}\n')
			else:
				direction = +1 if prev_x < x else -1
				prev_x -= (prev_x - x) % step * direction
				if abs(prev_x - x) < 1e-6:
					continue
				#print(direction, prev_x, x, abs(prev_x - x))
				nx = prev_x + step * direction
				while True:
					start = '' if cmd is None else (cmd + ' ')
					assert y is None
					_ = f.write(f'{start}X{round(nx, 2)}\n')
					_ = f.write('M106\n')
					_ = f.write(f'G4 P{int(s*laser_max_msec)}\n')
					_ = f.write('M107 P1\n')
					c = int(s*255)
					xy = int(x*10 * 0.1 / step), sz - 1 - int(prev_y*10 * 0.1 / step)
					#print('=',sz, xy)
					c = 0 if xy[0] % 2 == 0 else 255
					#print(xy, c)
					img.putpixel(xy, (c, c, c))
					if abs(nx - x) < 1e-6:
						break
					nx = nx + step * direction


#TODO check img.paste pastes where we need it
img.save("res.tiff", compression=None)  #, resolution_unit='inch', dpi = (RES_X, RES_Y))

'''
G0 X101.15 Y196.83 S0.0000
G1 X101.25 S0.4039
X105.05 S0.8588
X105.25 S0.8026


line = 'G0 X101.15 Y196.83 S0.0000'
cmd, x, y, s = parse(line)
print(cmd, x, y, s)
prev_x, prev_y = x, y
line = 'X105.05 S0.8588'
cmd, x, y, s = parse(line)
print(cmd, x, y, s)

step = 0.2
direction = +1 if prev_x < x else -1
prev_x -= (prev_x - x) % step * direction
print(abs(prev_x - x) < 1e-6)
print(direction, prev_x, x, abs(prev_x - x))
nx = prev_x + step * direction
'''