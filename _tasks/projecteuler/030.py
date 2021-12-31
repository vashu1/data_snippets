# Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.

powers5 = {str(i):i**5 for i in range(10)}

max_n = 9**5 * 6

res = 0
for n in range(2, max_n+1):
    s = sum([powers5[c] for c in str(n)])
    if n == s:
        print(n)
        res += n

print(res)