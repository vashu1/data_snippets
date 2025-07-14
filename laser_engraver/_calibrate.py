step = 0.2

print('G91 ; Set all axes to relative\n')

for i in range(10):
	c = i * 5
	for y in range(5):
		print(f'G1 Y{step}')
		for x in range(5):
			print(f'G1 X{step}')
			print('M106')
			print(f'G4 P{c}')
			print('M107 P1')