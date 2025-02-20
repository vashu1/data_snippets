from RefractionShift.refraction_shift import refraction
import math
import numpy as np


T_0 = 273.15 + 10 # temperature at the observer (K)
P_0 = 101_325 # pressure at the observer (Pa)
h0 = 0 # altitude at the observer (m)
lmbda =  550e-9 # Wavelength (m)
#lmbda =  700e-9 # RED
#lmbda =  470e-9 # BLUE
z0_deg = 89 # zenith angle (deg) 

MAX_H = 80_000  # m
STEP_LENGTH_M = 1_000  # m

sign = lambda v: 1 if v > 0 else -1

ATMOSPHERIC_REFRACTION = {  # from https://ru.wikipedia.org/wiki/%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D1%80%D0%B5%D1%84%D1%80%D0%B0%D0%BA%D1%86%D0%B8%D1%8F
	90: 0, 
	70: 0.4,
	50: 0.8,
	30: 1.7,
	20: 2.6,
	10: 5.3,
	5: 	9.9,
	4: 	11.8,
	3: 	14.4,
	2: 	18.4,
	1: 	24.7,
}

## Create an instance of the class LateralShift



#z0 = np.deg2rad(z0_deg) # zenith angle (rad)


def calc(h0, angle, earth=False, lmbda=lmbda):  # angle 0 = horizontal
	Refraction = refraction(T_0, P_0, h0)
	r_index = lambda h: Refraction.refraction_index(h, lmbda)[0]
	h = h0
	a = np.deg2rad(angle)
	s = 0
	sda = 0
	below10 = 0
	max_h = 0
	while True:
		dh = STEP_LENGTH_M * math.sin(a)
		h += dh
		ds = STEP_LENGTH_M * math.cos(a)
		s += ds
		if h < 10_000:
			below10 += ds
		max_h = max(max_h, h)
		if earth:
			da = ds / 4e7 * 2 * math.pi
			sda += da
			a += da
			#earth = False
			#print('- a ds da', a, ds, ds / 4e7 * 2 * math.pi)
		n0 = r_index(h)
		n1 = r_index(h + dh)
		cos_a1 = n0 / n1 * math.cos(a)
		if h < 0:
			#print('stop meters', round(s), 'below10', round(below10), 'max_h', round(max_h))
			return round(s)
		#if abs(cos_a1) > 1:  # TODO stop at h0
		#	print('down meters', round(2*s), dh, a, round(below10), max_h)
		#	return 0
		a = math.acos(cos_a1) * sign(a) if cos_a1 < 1 else -1e6
		if h > MAX_H:
			a -= sda
			arcmins = (angle - np.rad2deg(a)) * 60
			print('out arcmins', (np.rad2deg(a) - angle) * 60)
			return arcmins


s = calc(h0=2, angle=1.362)
print(s, 1.362*60)
exit(0)

a = 0
n = 0
while True:
	a += 1/60
	n += 1
	#s = calc(h0=2, angle=a)
	#print(n, s)
	s1 = calc(h0=2, angle=a, lmbda=700e-9)
	s2 = calc(h0=2, angle=a, lmbda=470e-9)
	print(n, s1, s2, round((s1-s2)/s1* 100, 2))
	if a > 1.37:
		break

print(s)

# TODO negative angles
#s = calc(h0=1_000, zenith_angle=89.5)
#s = calc(h0=1_000, zenith_angle=89.0)

exit(0)

# Earth with zero curvative
STEP_LENGTH_M = 10
h0 = 0
dh = (2e7 ** 2 + STEP_LENGTH_M ** 2) ** 0.5 - 2e7
Refraction = refraction(T_0, P_0, h0)
r_index = lambda h: Refraction.refraction_index(h, lmbda)[0]
n0 = r_index(h0)
n1 = r_index(h0 + dh)
cos_a1 = n1 / n0
a = math.acos(cos_a1)
print(a, STEP_LENGTH_M / 4e7 * 2 * math.pi, STEP_LENGTH_M / 4e7 * 2 * math.pi / a)

# >>> 2.7**(13700/8560)
#4.90211612021143

#exit(0)

#TEST
for k, v in ATMOSPHERIC_REFRACTION.items():
	arcmins = calc(1, k, earth=True)
	print(k, v, round(arcmins, 1), round((v - arcmins) / v * 100, 1) if v > 0 else 0, '%')
