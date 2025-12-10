

test = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''

data = test.split('\n')
data = [s.strip() for s in open('01.txt').readlines()]

dial = 50
cnt = 0
for s in data:
	s = s.replace('R', '+').replace('L', '-')
	s = int(s)
	dial = (dial + s) % 100
	if dial == 0:
		cnt += 1

print(cnt)

# II

sign = lambda x: +1 if x > 0 else -1

dial = 50
cnt = 0
for s in data:
	s = s.replace('R', '+').replace('L', '-')
	s = int(s)
	for i in range(abs(s)):
		dial = (dial + sign(s)) % 100
		if dial == 0:
			cnt += 1

print(cnt)