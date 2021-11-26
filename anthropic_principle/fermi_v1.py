# --upgrade pip --user
# pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org matplotlib
# pip install matplotlib config --global http.sslVerify false
"""
def sigm(x):
  y = 1/(1+math.exp(-x))
  return y

def sigm_r(y):
  x = math.log(y/(1-y))
  return x
"""
import math
import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np

def end_p(t, period):  # t in Gy
  return 2**(-t/period)

def norm(x):
    # normalise x to range [0,1]
    nom = (x - x.min()) * 1.0
    denom = x.max() - x.min()
    return  nom/denom

def sigmoid(x, k=1):
    # sigmoid function
    # use k to adjust the slope
    s = 1 / (1 + np.exp(-x / k))
    return s

def f(start_y, sigmoid_k, end_period):
  total_gy = max(40, start_y*2)
  dots_per_gy = 10
  xs = np.array([x/dots_per_gy for x in range(total_gy*dots_per_gy)])  # 0 to total_gy Gy
  ys = sigmoid(xs[:start_y*dots_per_gy*2]-start_y, k=sigmoid_k)
  ys = norm(ys)
  ys = np.concatenate((ys, np.ones((total_gy-start_y*2)*dots_per_gy)))
  if end_period:
    ys *= end_p(xs, end_period)
  i = len(ys)
  while ys[i-1] == 1:
    i -= 1
  return xs[:i], ys[:i]

def plot(a,b,c, w=1):
  xs, ys = f(a,b,c)
  s = ys[1:] - ys[:-1]
  s = s.clip(min=0)
  if True:
      xs2, ys2 = f(a,b,None)  # no catastrophes for width
      if ys2[-1] > 0.9:
        s2 = ys2[1:] - ys2[:-1]
        s2 = s2.clip(min=0)
      print('w', sum(s2[(a-w)*10:(a+w)*10])/sum(s2))
  print('earth', sum(s[:45])/sum(s), '6gy', sum(s[:60])/sum(s[:45]), '7gy', sum(s[:70])/sum(s[:45]), '8gy', sum(s[:80])/sum(s[:45]))
  plt.plot(xs, ys)
  plt.show()

plot(8, 0.6, None)

"""
xs, ys = f(5, 1, 1)
s = ys[1:] - ys[:-1]
print(sum(s[:50])/sum(s))
plt.plot(xs[:-1], ys)
plt.show()
"""
