import os

data = []
triangles = []
txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
for line in open(txt_name).readlines():
    vals = [int(c) for c in line.strip().split(' ') if c]
    data.append(vals)
    a, b, c = sorted(vals)
    if a + b > c:
        triangles.append((a, b, c))

print(len(triangles), len(set(triangles)))

cc = 0
triangles = []
for y in range(0, len(data), 3):
    for x in range(3):
        a, b, c = data[y][x], data[y+1][x], data[y+2][x]
        a, b, c = sorted([a, b, c])
        cc += 1
        if a + b > c:
            triangles.append((a, b, c))

#print(len(data), cc)
print(len(triangles), len(set(triangles)))
