import numpy as np

v =  ''.join(['.']+[str(n) for n in range(1, 300_000)])
assert v[12] == '1'
assert len(v) > 1_000_000

vals = [v[10**i] for i in range(6+1)]
assert len(vals) == 7

print(np.prod(list(map(int, vals))))