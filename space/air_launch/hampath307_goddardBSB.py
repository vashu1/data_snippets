# Main file for the Bang-Sinular-Bang case for Goddard problem
#
# Problem definition
#
#   max h(tf)
#   dot(h) = v
#   dox(v) = (u-D)/m - 1/r**2
#   dot(m) = -u
#   h(0) = h_0, v(0) = v_0, m(0) = m_0, m(1) = m_f
#
#  \author Olivier Cots & Jean-Matthieu Khoury (INP-ENSEEIHT-IRIT)
#  \date   2016
#
import numpy as np
import matplotlib.pyplot as plt
# It is assumed that HamPath lib files are placed in LIBHAMPATH
from LIBHAMPATH.hampathcode import *
from LIBHAMPATH.control_p import *
from LIBHAMPATH.geth1_p import *
from LIBHAMPATH.geth01_p import *

#-------------------------------------------------------------------------------------------------------------%
print('\nStep 1: parameters initialization\n')

# Initial guess
t0      = 0.0                               # Initial time
t0norm  = 0.0                               # Normalized initial time
tf      = 206.661                           # Final time
tfnorm  = 1.0                               # Normalized final time
t1      = 4.1211968208713                   # First guessed switching time
t1norm  = (t1-t0)/(tf-t0)                   # Normalized first guessed switching time
t2      = 45.9573259680671                  # Second guessed switching time
t2norm  = (t2-t0)/(tf-t0)                   # Normalized second guessed switching time
q0      = np.array([0.0,0.0,214.839])       # Initial state h_0 v_0 m_0
n       = len(q0)                           # State dimension
p0      = np.array([0.945632204560262E+01, 0.205487457284517E+03, 0.175867755658218E+04])
par     = np.array([tf, 0.01227, 0.000145, 9.81, 9.52551, 2060, t0, q0[0], q0[1], q0[2], 67.9833,1,2,0])  # tf, alpha, beta, g0, umax, c, t0, q0, mf
npar    = len(par)
options = HampathOptions()                  # Hampath options
print(options)

# Initial guess
z0          = np.zeros((2*n,))
z0[0:n]     = q0
z0[n:2*n]   = p0
[ tout, z, flag] = exphvfun(np.array([t0norm,t1norm,t2norm]), z0, np.array([t0norm, t1norm, t2norm, tfnorm]), options, par)
z1          = z[:,1]                    # z1 = integration of z0 between t0 and t1
z2          = z[:,2]                    # z2 = integration of z0 between t1 and t2
yGuess          = np.zeros((17,))
yGuess[0:3]     = p0                        # yGuess = [p0, t1, z1, t2, z2]
yGuess[3]       = t1
yGuess[4:10]    = z1
yGuess[10]      = t2
yGuess[11:17]   = z2

#-------------------------------------------------------------------------------------------------------------%
print('\nStep 2: first shooting\n')

[y0,ssol,nfev,njev,flag] = ssolve(yGuess,options,par)

#-------------------------------------------------------------------------------------------------------------%
print('\nStep 3: plotting the solution\n')

fig, axarr = plt.subplots(nrows=2, ncols=5)
#fig.tight_layout() # Or equivalently,  "plt.tight_layout()"

left    = 0.125 # the left side of the subplots of the figure
right   = 0.9   # the right side of the subplots of the figure
bottom  = 0.1   # the bottom of the subplots of the figure
top     = 0.9   # the top of the subplots of the figure
wspace  = 0.3   # the amount of width reserved for blank space between subplots
hspace  = 0.3   # the amount of height reserved for white space between subplots

fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

# Solution
z0          = np.zeros((2*n,))
z0[0:n]     = q0
z0[n:2*n]   = y0[0:3]
t1          = y0[3]
t2          = y0[10]
t1norm      = (t1-t0)/(tf-t0)
t2norm      = (t2-t0)/(tf-t0)
ti          = np.array([t0norm,t1norm,t2norm,tfnorm])
[ tout, z, flag ] = exphvfun(np.array([t0norm, tfnorm]), z0, ti, options, par)
lig,col = 0,0;
axarr[lig,col].plot(tout,z[0,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$h$')  ; axarr[lig,col].set_title('State solution')
lig,col = 1,0;
axarr[lig,col].plot(tout,z[3,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$p_h$'); axarr[lig,col].set_title('Co-state solution')
lig,col = 0,1; axarr[lig,col].plot(tout,z[1,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$v$')
lig,col = 1,1; axarr[lig,col].plot(tout,z[4,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$p_v$')
lig,col = 0,2; axarr[lig,col].plot(tout,z[2,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$m$')
lig,col = 1,2; axarr[lig,col].plot(tout,z[5,:],'b'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$p_m$')

# Control
u   = control(tout,z,ti,par)
lig,col = 0,3; axarr[lig,col].plot(tout,u[0,:],'r'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$u$'); axarr[lig,col].set_title('Control')

# H1
zer = np.zeros((len(tout)))
H1  = geth1(tout,z,ti,par)
lig,col = 0,4; axarr[lig,col].plot(tout,H1[0,:],'g'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$H_1$');
axarr[lig,col].set_title('$H_1$'); axarr[lig,col].plot(tout,zer,'--')

# H01
H01 = geth01(tout,z,ti,par)
lig,col = 1,4; axarr[lig,col].plot(tout,H01[0,:],'g'); axarr[lig,col].set_xlabel('t'); axarr[lig,col].set_ylabel('$H_{01}$');
axarr[lig,col].set_title('$H_{01}$'); axarr[lig,col].plot(tout,zer,'--')

#-------------------------------------------------------------------------------------------------------------%
axarr[1, 3].axis('off')
plt.show()
