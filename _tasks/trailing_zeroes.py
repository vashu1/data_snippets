"""
Trailing zeros
input = 110
output = 2

input = 1230430000
output = 6
input = 12300000
output = 3
"""

def tr_zeroes(N: int) -> int:
    positive_n = abs(N)
    n_str = str(positive_n)
    #if n_str.startswith('-'):  # negative
    #    n_str = n_str[1:]
    count = 0
    for indx in range(len(n_str)-1, 0-1, -1):
        if n_str[indx] == '0':
            count += 1
        else:
            return len(n_str) - count
    return 0

print(tr_zeroes(110))
print(tr_zeroes(1230430000))
print(tr_zeroes(12300000))
print(tr_zeroes(-10))
print(tr_zeroes(0))