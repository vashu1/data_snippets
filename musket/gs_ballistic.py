from array import array
from math import *

feetToMeter = 0.3048
poundToKg = 0.453592

#DIAMETER=125
DIAMETER = 55#18 # mm    1000 = 1 m
DENSITY = 5.5 #11.3 # kg/l    5.5 = density of iron    11.3 - lead
SPEED = 450 # m/s  320 - speed of sound
ELEVATION_D = 0 # degrees
ELEVATION_Y = 2 # meters
DISTANCE_STEP = 20 # meters

# ALGORITM SOURCE
# http://www.frfrogspad.com/coefdrag.gif
# http://arc.id.au/CannonBallistics.html
# http://arc.id.au/CannonballDrag.html

# DRAG TABLE SOURCE
# http://www.snipercountry.com/ballistics/software/mctraj4.zip
# GS ballistics raw - even indexes are speed in thousands of ft per sec, odd are ballistic coeff.

# TEST
# http://www.frfrogspad.com/extbal2.htm#Shotgun
# A 75 yd "zero" is assumed
# 00 buckshot: 3.48 gr, with a diameter of about 8.4 mm (.33 inch).
# SETTINGS:
# DIAMETER = 8.4 # mm    1000 = 1 m
# DENSITY = 11.3 # kg/l   11.3 - lead
# SPEED = 1290*feetToMeter # m/s  320 - speed of sound
# ELEVATION_D = 0.1 # degrees
# ELEVATION_Y = 10 # meters
# DISTANCE_STEP = 22.5 # meters
# Calculated: Weight(kg) = 0.00350683170222
# Data
# Range(ya)	V(ya/s)		Calculated
# 0				1290		1290
# 25			1050		1068
# 50			930			909
# 75			840			790
# 100			770			697
# 125			710			621
# 150			610			558
# relative error less that 10%(partially explained by different GS for small projectiles)

gsTable = array('d', [0.00  ,  0.4662, 0.05  ,  0.4689, 0.10  ,  0.4717, 0.15  ,  0.4745, 0.20  ,  0.4772, 0.25  ,  0.4800, 0.30  ,  0.4827, 0.35  ,  0.4852, 0.40  ,  0.4882, 0.45  ,  0.4920, 0.50  ,  0.4970, 0.55  ,  0.5080, 0.60  ,  0.5260, 0.65  ,  0.5590, 0.70  ,  0.5920, 0.75  ,  0.6258, 0.80  ,  0.6610, 0.85  ,  0.6985, 0.90  ,  0.7370, 0.95  ,  0.7757, 1.0   ,  0.8140, 1.05  ,  0.8512, 1.10  ,  0.8870, 1.15  ,  0.9210, 1.20  ,  0.9510, 1.25  ,  0.9740, 1.30  ,  0.9910, 1.35  ,  0.9990, 1.40  ,  1.0030, 1.45  ,  1.0060, 1.50  ,  1.0080, 1.55  ,  1.0090, 1.60  ,  1.0090, 1.65  ,  1.0090, 1.70  ,  1.0090, 1.75  ,  1.0080, 1.80  ,  1.0070, 1.85  ,  1.0060, 1.90  ,  1.0040, 1.95  ,  1.0025, 2.00  ,  1.0010, 2.05  ,  0.9990, 2.10  ,  0.9970, 2.15  ,  0.9956, 2.20  ,  0.9940, 2.25  ,  0.9916, 2.30  ,  0.9890, 2.35  ,  0.9869, 2.40  ,  0.9850, 2.45  ,  0.9830, 2.50  ,  0.9810, 2.55  ,  0.9790, 2.60  ,  0.9770, 2.65  ,  0.9750, 2.70  ,  0.9730, 2.75  ,  0.9710, 2.80  ,  0.9690, 2.85  ,  0.9670, 2.90  ,  0.9650, 2.95  ,  0.9630, 3.00  ,  0.9610, 3.05  ,  0.9589, 3.10  ,  0.9570, 3.15  ,  0.9555, 3.20  ,  0.9540, 3.25  ,  0.9520, 3.30  ,  0.9500, 3.35  ,  0.9485, 3.40  ,  0.9470, 3.45  ,  0.9450, 3.50  ,  0.9430, 3.55  ,  0.9414, 3.60  ,  0.9400, 3.65  ,  0.9385, 3.70  ,  0.9370, 3.75  ,  0.9355, 3.80  ,  0.9340, 3.85  ,  0.9325, 3.90  ,  0.9310, 3.95  ,  0.9295, 4.00  ,  0.9280]);
gsTableLength = gsTable.buffer_info()[1];

# drag coefficien for any shrapnel shape
# FRAGMENTATION AND LETHALITY ANALISYS
# Ballistics 2013: 27th International Symposium on Ballistics, p. 665
# http://books.google.ru/books?id=7cdm9VOpB1oC&pg=PA668&lpg=PA668&dq=shrapnel+drag-function&source=bl&ots=fUdAkYPbx2&sig=X8qSKXfnX4XgzEAY9sYsV4d7eOg&hl=en&sa=X&ei=MwdtUp-ADqvU4wS2q4HYDw&ved=0CCUQ6AEwAA#v=onepage&q=shrapnel%20drag-function&f=false
# on subsonic speed it slightly worse than sphere
# on supersonic less than 10% better(sharp eges I'd guess)

def GSapprox(feetPerSecond):
	tableSpeed = feetPerSecond*feetToMeter / 320.0 # ratio to sound speed
	if(tableSpeed<0):
		raise Exception('GSapprox: negative speed');
	if(tableSpeed>=gsTable[gsTableLength-2]):
		raise Exception('GSapprox: too big speed');
	for i in range(0, gsTableLength-1, 2):
		if( (gsTable[i] <= tableSpeed) and (tableSpeed < gsTable[i+2]) ):
			return gsTable[i+1] + (tableSpeed-gsTable[i])/(gsTable[i+2]-gsTable[i])*(gsTable[i+3]-gsTable[i+1]);

def plotShrapnel(d, m, u, theta, y0):
	g = 0#32.2;            # acceleration due to gravity (9.8 m/s)
	rho = 0.074;         # density of air  (1.225 kg/m^3)
	phi = 3.158E-5;      # atm density scale factor (9.626E-6 /m)
	#Cd, decel, H;        # drag coeff, deceleration, altitude factor
	x = 0.0;               # range
	y = y0;              # height
	V = u;               # magnitude of velocity vector
	vx = V*cos(pi*theta/180.0); # x vel component
	vy = V*sin(pi*theta/180.0);
	#ax, ay;              # acceleration components
	dt = 0.0001;           # time step size
	distanceMark = 0;
	while (y>0):    # stop track when bullet hits ground
		Cd = GSapprox(V);
		H = exp(-phi*y);
		decel = Cd*rho*H*pi*d*d/(m*8.0);
		ax = -decel*V*vx;
		ay = -g -decel*V*vy;
		vx = vx + ax*dt;
		vy = vy + ay*dt;
		V = sqrt(vx*vx+vy*vy);
		x = x + vx*dt + ax*dt*dt/2.0;
		y = y + vy*dt + ay*dt*dt/2.0;
		if((x*feetToMeter)>(distanceMark)):
			distanceMark += DISTANCE_STEP;
			print("Distance: " + str(round(x*feetToMeter)) + "(" + str(round(x/3.0)) + " ya) Speed: " + str(round(V*feetToMeter)) + "(" + str(round(V)) + \
				" ft/s) Energy: " + str(round((V*feetToMeter)*(V*feetToMeter)*(m*poundToKg)/2.0)) + \
				"  Height=" + str(round(y*feetToMeter)))
	print("  Range = "+str(round(x*feetToMeter))+" m")

def printShrapnel(speed, diam, density):
	volume = (4.0/3.0)*pi*diam*diam*diam/8.0; # m^3
	weight = density*volume*1000.0;
	print("Volume(lt) = " + str(volume*1000.0))
	print("Speed(m/s) = " + str(speed))
	print("Weight(kg) = " + str(weight))
	plotShrapnel(diam/feetToMeter, weight/poundToKg, speed / feetToMeter, ELEVATION_D, ELEVATION_Y / feetToMeter);


printShrapnel(SPEED, DIAMETER/1000.0, DENSITY)
