# find d of droplet where surface energy == energy of evaporation
import math
import scipy.optimize
EVAPORATION_ENERGY = 2.5*1e6 # J
ST_K = 70 # N/m2  temperature https://www.engineeringtoolbox.com/surface-tension-d_962.html
mass = lambda d: d**3 * math.pi / 6 * 1000 # kg
surface_energy = lambda d: math.pi * (d ** 2) * ST_K # J
func = lambda d: 1 - mass(d)*EVAPORATION_ENERGY / surface_energy(d)
d = scipy.optimize.newton(func, 1e-3) # start from 1 mm
print(f'd = {d:.1e} m')
