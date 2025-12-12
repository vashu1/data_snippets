
data = [s.strip() for s in open('12.txt').readlines()]

weights = [5,7,6,7,7,7]

c = 0
rs = []
for line in data:
	if 'x' not in line:
		continue
	sz, v = line.split(': ')
	a, b = sz.split('x')
	a = int(a)
	b = int(b)
	v = sum([int(i)*weights[indx] for indx, i in enumerate(v.split(' '))])
	r = v/(a*b)
	print(r)
	rs.append(r)
	if r < 1:
		c += 1

print(max([r for r in rs if r<1]))
print(list(sorted(([-r for r in rs if r<1]))))

print(c)
