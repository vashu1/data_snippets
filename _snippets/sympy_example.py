# https://kobak.livejournal.com/131743.html#t3582879
import numpy as np
from functools import reduce
from collections import defaultdict, Counter
from sympy import *
init_printing(use_unicode=True)

d1, d2, a, b = symbols('d1 d2 a b', real=True)

m = Matrix([[d1, a], [b, d2]])
#m = m * m.T
m = m * m * m.T * m.T
#m = m * m * m * m.T * m.T * m.T
n = m.norm() ** 2
n = n.expand()

spread = defaultdict(list)
for i in n.as_expr().args:
  powers = [(1 if j.is_Symbol else j.exp) for j in i.as_ordered_factors() if not j.is_Number]
  powers = tuple(sorted(powers))
  spread[powers].append(i)

spread = {k:reduce(Add, v, 0) for k, v in spread.items()}

result = Counter()
d = 2
N = 10_000
for i in range(N):
  np.random.seed(i)
  X = np.random.randn(d * d) / np.sqrt(d)
  for k, v in spread.items():
    result[k] += v.evalf(subs={k:v for k, v in zip([d1, d2, a, b], X)})

result = {k:v/N for k, v in result.most_common()}
for k, v in result.items():
  print(k, round(v, 2))
