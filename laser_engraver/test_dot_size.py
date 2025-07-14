impulse = 350
dot_size = 0.4

square_size = 16

with open(f't_{impulse}_{dot_size}.gcode', 'w') as f:
	printf = lambda txt: print(txt, file=f, end='\n')
	printf('G21         ; Set units to mm')
	printf('G90         ; Absolute positioning')
	for y in range(square_size):
		for x in range(square_size):
			printf(f'G1 X{dot_size*x} Y{dot_size*y}')
			printf('M106')
			printf(f'G4 P{impulse}')
			printf('M107 P1')
	printf('G1 X0 Y0')
	printf('M84         ; Disable motors')
