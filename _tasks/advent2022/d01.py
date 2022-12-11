
data1 = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

data1 = ''.join(open('d01.txt').readlines())

lst = []
acc = 0
for line in data1.split('\n'):
    if not line.strip():
        lst.append(acc)
        acc = 0
        continue
    calories = int(line)
    acc += calories

if acc:
    lst.append(acc)

lst.sort()

print(lst)
print(max(lst))
print(lst[-3:])
print(sum(lst[-3:]))