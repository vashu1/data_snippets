'''

By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.

odd even (odd odd) even (odd odd) even odd ...
'''

fibs = [1, 2]
while fibs[-1] <= 4_000_000:
    fibs.append(fibs[-1] + fibs[-2])

_ = fibs.pop()
print(sum([v for v in fibs if v%2 == 0]))