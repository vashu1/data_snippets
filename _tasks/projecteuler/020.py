# Find the sum of the digits in the number 100!

res = 1
for n in range(1, 100+1):
    res *= n

print(sum(map(int, str(res))))