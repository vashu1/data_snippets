# heating of air with adiabatic compression
import scipy.optimize

Tstart = 10+273.15 # 10 C
Kair = 1.4

def get_t(Tstart, Pstart, Pend): # Newton's method
    const = (Pstart ** (1 - Kair)) * (Tstart ** Kair)  # P–T relation for adiabatic heating and cooling
    func = lambda t: const - (Pend ** (1 - Kair)) * (t ** Kair)
    return scipy.optimize.newton(func, Tstart)

""" TEST
# https://studme.org/273851/tehnika/ohlazhdenie_rasshirenii_gazov
# Если воздух, сжатый до 9,5 МПа при t{ = 20°С, адиабатно расширяется до 0,1 МПа, то при k = 1,4 его конечная температура t2 = -193,4°С.
>>> get_t(293, 95, 1)
79.76341380496662
>>> 273-193
80
"""

print('T\tP drop')
for i in range(2,11+1):
    print(f'{i-1}\t{round(Tstart - get_t(Tstart, i, 1),1)}')