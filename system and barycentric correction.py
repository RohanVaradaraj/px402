# Load in libraries
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import interpolate

# Enter folder with spectra to load them in.
os.chdir(r'C:\Users\Rohan\PycharmProjects\PX402\Spectra arrays');

'''AUGUST'''

n_spectra = 31 # 29 replace as necessary
# 31 = AUGUST, 29 = SEPTEMBER

# Load in some data
fluxes_A_aug = np.load('fluxes_A_aug.npy')
wlen_aug = np.load('wlen_soln_aug.npy')
hier_berv_aug = np.load('hier_berv_aug.npy') # in km/s


# Define the system velocity
v_sys =  -9.62826 # +/- 0.00023 km/s

# Define the speed of light
c_light = 299792.458 # in kms

# Create radial velocity vector.
rad_vel_aug = np.zeros(n_spectra)

# Fill radial velocity vector
for i in range(0, n_spectra):
    rad_vel_aug[i] = v_sys - hier_berv_aug[i]
    
# Create corrected wavelength vector
wlen_dopp_aug = np.zeros((n_spectra,4080))

# Correct for Doppler shift
for spec_i in range(0, n_spectra):
    for wlen_i in range(0, 4080):
        wlen_dopp_aug[spec_i, wlen_i] = wlen_aug[wlen_i] * ( 1 + (rad_vel_aug[spec_i] / c_light))
        
# # Try interpolation method
newflux_A_aug = np.zeros((n_spectra, 4080))
for i in range(0, n_spectra):
    interp_A_aug = interpolate.splrep(wlen_aug, fluxes_A_aug[i,])
    newflux_A_aug[i,] = interpolate.splev(wlen_dopp_aug[i,], interp_A_aug)    

    
'''SEPTEMBER'''
    
# REDEFINE N_SPECTRA
n_spectra =  29

# Load in some data
fluxes_A_sep = np.load('fluxes_A_sep.npy')
hier_berv_sep = np.load('hier_berv_sep.npy') # in km/s
wlen_sep = np.load('wlen_soln_sep.npy')

# Plot using imshow
# plt.imshow(fluxes_A_aug, aspect='auto')

# Create radial velocity vector.
rad_vel_sep = np.zeros(n_spectra)

# Fill radial velocity vector
for i in range(0, n_spectra):
    rad_vel_sep[i] = v_sys - hier_berv_sep[i]
    
# Create corrected wavelength vector
wlen_dopp_sep = np.zeros((n_spectra, 4080))

# Correct for Doppler shift
for spec_i in range(0, n_spectra):
    for wlen_i in range(0, 4080):
        wlen_dopp_sep[spec_i, wlen_i] = wlen_sep[wlen_i] * ( 1 + (rad_vel_sep[spec_i] / c_light))
        
# # # Try interpolation method
newflux_A_sep = np.zeros((n_spectra, 4080))
for i in range(0, n_spectra):
    interp_A_sep = interpolate.splrep(wlen_sep, fluxes_A_sep[i,])
    newflux_A_sep[i,:] = interpolate.splev(wlen_dopp_sep[i,], interp_A_sep)  

    
# CHECKS WITH PLOTTING 
# Plot all spectra
for i in range(0, n_spectra):
    plt.plot(wlen_aug[300:500], newflux_A_aug[i,300:500]) 
    
for i in range(0, n_spectra):
    plt.plot(wlen_sep[300:500], newflux_A_sep[i,300:500]) 

# plt.plot(wlen_dopp_aug, fluxes_A_aug[4,:]-0.03)
    
# Save shifted wavelength solution.
np.save('wlen_dopp_aug', wlen_dopp_aug)
np.save('wlen_dopp_sep', wlen_dopp_sep)

print(np.mean(hier_berv_aug))
print(np.mean(hier_berv_sep))