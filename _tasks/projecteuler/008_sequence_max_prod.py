import numpy as np

number = '''73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450'''
number = ''.join(number.split('\n'))

N = 13
max_prod = 0
for i in range(len(number)-N+1):
    vals = number[i:i+N]
    vals = [int(v) for v in vals]
    prod = np.prod(vals)
    if prod > max_prod:
        max_prod = prod

if __name__ == '__main__':
    print(max_prod)

# TRY 2

def sequence_max_prod(numbers, N):
    vals = numbers[0:0+N]
    zeroes_count = len(vals[vals == 0])
    prod = np.prod([(v if v>0 else 1) for v in vals])
    max_prod = 0 if zeroes_count else prod
    for i in range(len(numbers)-N):
        drop_v = numbers[i]
        if drop_v == 0:
            zeroes_count -= 1
            drop_v = 1
        prod //= drop_v
        add_v = numbers[i+N]
        if add_v == 0:
            zeroes_count += 1
            add_v = 1
        prod *= add_v
        if zeroes_count == 0 and prod > max_prod:
            max_prod = prod
    return max_prod

if __name__ == '__main__':
    numbers = np.array([int(v) for v in number])
    print(sequence_max_prod(numbers, N))