
'''

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

'''

print(sum([i for i in range(1000) if (i%3==0) or (i%5==0)]))

'''
#generate powers of 5 and 3

def generate_multiples_3_5(threshold, c3=0, c5=0):
    result = (3**c3) * (5**c5)
    #print(f'{c3=} {c5=} {result=}')
    if result >= threshold:
        if c3 != 0:
            yield from generate_multiples_3_5(threshold, c3=0, c5=c5 + 1)  # iterate next c5
        return
    if result > 1:
        yield result
    yield from generate_multiples_3_5(threshold, c3=c3 + 1, c5=c5)

print(list(generate_multiples_3_5(10)))
print(sum(generate_multiples_3_5(1000)))

import math
threshold = 1000
max5 = int(math.log(threshold, 5))+1
max3 = int(math.log(threshold, 3))+1
vals = [(3**c3) * (5**c5) for c3 in range(max3) for c5 in range(max5) if (c3>0 or c5>0)]
print(sum(set([v for v in vals if v < threshold])))
'''