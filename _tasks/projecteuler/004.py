'''
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
'''

vals = [str(i*j) for i in range(1000) for j in range(1000)]
vals = [v for v in vals if v == v[::-1]]
vals = [int(v) for v in vals]
vals.sort()
print(vals[-1])
