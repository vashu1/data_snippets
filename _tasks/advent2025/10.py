
test = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''

data = test.split('\n')
data = [s.strip() for s in open('10.txt').readlines()]


def parse_button(s):
	t = eval(s.replace(')', ',)'))
	res = 0
	for i in t:
		i = int(i)
		res |= 2 ** i
	return res

s = 0
for line in data:
	indicator_str, buttons = line.split('] ')
	indicator_str = indicator_str[1:]
	buttons = buttons.split(' {')[0].split(' ')
	indicators_len, indicators = len(indicator_str), eval('0b' + indicator_str.replace('.', '0').replace('#', '1')[::-1])
	buttons = [parse_button(s) for s in buttons]
	solution_pressed = 1_000
	for i in range(2 ** len(buttons)):
		indicator_result, button_presses = 0, 0
		for j in range(len(buttons)):
			if i & (2 ** j):
				indicator_result ^= buttons[j]
				button_presses += 1
		if indicator_result == indicators:
			solution_pressed = min(solution_pressed, button_presses)
	assert solution_pressed != 1_000
	s += solution_pressed

print(s)