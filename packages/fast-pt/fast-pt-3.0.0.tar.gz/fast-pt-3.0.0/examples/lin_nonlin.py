
"""An example script to run FASTPT
Initializes and calculates all quantities supported by FASTPT
Makes a plot for P_22 + P_13
"""
from time import time

from Cosmo_JAB import cosmo
import numpy as np
import matplotlib.pyplot as plt

import fastpt as fpt
from fastpt import FASTPT

#Version check
print('This is FAST-PT version', fpt.__version__)

# load the data file

#d=np.loadtxt('Pk_test.dat')
d=np.loadtxt('stream_velocity_lin_matterpower_z0.dat')
dhf=np.loadtxt('stream_velocity_HF_matterpower_z0.dat')
# declare k and the power spectrum
k=d[:-1,0]; P=d[:-1,1]
Phf=dhf[:-1,1]

# set the parameters for the power spectrum window and
# Fourier coefficient window
#P_window=np.array([.2,.2])
C_window=.75
#document this better in the user manual

# padding length
n_pad=int(0.5*len(k))
to_do=['one_loop_dd']

# initialize the FASTPT class
# including extrapolation to higher and lower k
# time the operation
t1=time()
fastpt=FASTPT(k,to_do=to_do,low_extrap=-5,high_extrap=3,n_pad=n_pad)
t2=time()

# calculate 1loop SPT (and time the operation)
P_spt=fastpt.one_loop_dd(P,C_window=C_window)

t3=time()
print('initialization time for', to_do, "%10.3f" %(t2-t1), 's')
print('one_loop_dd recurring time', "%10.3f" %(t3-t2), 's')

#calculate tidal torque EE and BB P(k)
#P_IA_tt=fastpt.IA_tt(P,C_window=C_window)
#P_IA_ta=fastpt.IA_ta(P,C_window=C_window)
#P_IA_mix=fastpt.IA_mix(P,C_window=C_window)
#P_RSD=fastpt.RSD_components(P,1.0,C_window=C_window)
#P_kPol=fastpt.kPol(P,C_window=C_window)
#P_OV=fastpt.OV(P,C_window=C_window)
#sig4=fastpt.sig4(P,C_window=C_window)

# make a plot of 1loop SPT results
omega_m_h2 = 0.14170
h = .6774
omega_m = omega_m_h2/h**2 
omega_l = 1.-omega_m

plt.rcParams["figure.figsize"] = (10,8)
for z in [10,6,4,2,1,0.5,0]:
    Growth = cosmo.Growth(z,Om_m0=omega_m,Om_l0=omega_l)
    ax=plt.subplot(111)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylabel(r'$P(k)$', size=15)
    ax.set_xlabel(r'$k$', size=15)
    ax.set_xlim([1e-4,1e2])
    ax.set_ylim([1e-3,5e4])
    
    ax.plot(k,Growth**2*P,label=r'$P_{lin},z=$'+str(z))
    ax.plot(k,Growth**2*P+Growth**4*P_spt[0], label=r'$P_{lin}+P_{22}+P_{13}$' )

    plt.legend(loc=3)
    plt.grid()
    plt.show()

ax=plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(r'$P(k)$', size=15)
ax.set_xlabel(r'$k$', size=15)
ax.set_xlim([1e-4,1e2])
ax.set_ylim([1e-3,5e4])
    
ax.plot(k,Growth**2*P,label=r'$P_{lin},z=$'+str(z))
ax.plot(k,Growth**2*P+Growth**4*P_spt[0], label=r'$P_{lin}+P_{22}+P_{13}$' )
ax.plot(k,Growth**2*Phf,label=r'$P_{NL}$')

plt.legend(loc=3)
plt.grid()
plt.show()    
