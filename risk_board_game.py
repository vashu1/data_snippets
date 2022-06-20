"""
Risk board game battle chances:

def_n=1 att_n=1 attacker loses: 58.33% wins: 41.67%
def_n=1 att_n=2 attacker loses: 42.13% wins: 57.87%
def_n=1 att_n=3 attacker loses: 34.03% wins: 65.97%
def_n=2 att_n=1 attacker loses: 74.54% wins: 25.46%
def_n=2 att_n=2 attacker loses: 44.83% wins: 22.76% dr: 32.41%
def_n=2 att_n=3 attacker loses: 29.26% wins: 37.17% dr: 33.58%
"""
from itertools import product

dice_values = list(range(1, 6 + 1))
for def_n in range(1, 2+1):
  dev_vals = list(product(*[dice_values for _ in range(def_n)]))
  for att_n in range(1, 3+1):
    att_vals = list(product(*[dice_values for _ in range(att_n)]))
    results = []
    for d in dev_vals:
      for a in att_vals:
        dd = list(sorted(d))
        aa = list(sorted(a))
        def1succ = dd[-1] >= aa[-1]
        res = 0
        res += -1 if def1succ else 1
        if len(dd) > 1 and len(aa) > 1:
          def2succ = dd[-2] >= aa[-2]
          res += -1 if def2succ else 1
        results.append(res)
    #print('len(results)', len(results))
    att_losses = len([i for i in results if i < 0])
    droughts = len([i for i in results if i == 0])
    att_wins = len([i for i in results if i > 0])
    att_losses = round(100 * att_losses / len(results), 2)
    droughts = round(100 * droughts / len(results), 2)
    att_wins = round(100 * att_wins / len(results), 2)
    print(f'{def_n=} {att_n=} attacker loses: {att_losses}% wins: {att_wins}%' + (f' dr: {droughts}%' if droughts else ''))
