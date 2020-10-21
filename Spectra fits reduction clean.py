### CLEAN CODE

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os

# Specify the file that contains the fits files.
# directory = r'C:\Users\Rohan\PycharmProjects\PX402\WASP-69_22-8-17' # AUGUST
directory = r'C:\Users\Rohan\PycharmProjects\PX402\WASP-69_22-9-17'   # SEPTEMBER

# Set working directory to data folder. This changes later when we save our numpy arrays.
# os.chdir(r'C:\Users\Rohan\PycharmProjects\PX402\WASP-69_22-8-17'); # AUGUST
os.chdir(r'C:\Users\Rohan\PycharmProjects\PX402\WASP-69_22-9-17');   # SEPTEMBER

# Take wavelength solution for the order that contains the 10830 Angstrom absorption line.
spec_aug = fits.open('C:/Users/Rohan/PycharmProjects/PX402/WASP-69_22-8-17/car-20170822T21h40m59s-sci-norl-nir_A.fits') 
spec_sep = fits.open('C:/Users/Rohan/PycharmProjects/PX402/WASP-69_22-9-17/car-20170922T20h32m48s-sci-norl-nir_A.fits')
# arbitrary file since wlen solutions are all basically the same.
wlen_aug = spec_aug[4].data
wlen_sep = spec_aug[4].data

# Initialize number of spectra
# n_spectra = 31 # AUGUST
n_spectra = 29   # SEPTEMBER

# INITIALIZE VECTORS
# Flux vectors
fluxes_A = np.zeros((n_spectra, 4080)) # Divide by 2 because we have A and B spectra.
fluxes_B = np.zeros((n_spectra, 4080))
fluxes_fibs = [fluxes_A, fluxes_B] # For looping later.

# wlen_mat_aug = np.zeros((n_spectra, 4080))
# wlen_mat_sep = np.zeros((n_spectra, 4080))

# Filenames lists
filenames_A = []
filenames_B = []
filenames_fibs = [filenames_A, filenames_B]
fibs = ['A', 'B']

# Header data vectors
mjd_obs =   np.zeros(n_spectra)
airmass =   np.zeros(n_spectra)
hier_bjd =  np.zeros(n_spectra)
hier_berv = np.zeros(n_spectra)

# Create lists of file names to be sorted by chronological order.
## This simply requires a regular sort() by virtue of the file names.
for fibs_i in range(0, 2):
    for file_i in os.listdir(directory):
        if fibs[fibs_i] in file_i:
            filenames_fibs[fibs_i].append(file_i)
            
# Sort chronologically
filenames_A.sort()
filenames_B.sort()

print(filenames_A)

# Collect data into a vector for each fibre
for fibs_i in range(0, 2):
    for spec_i in range(0, n_spectra):
        temp = fits.open(filenames_fibs[fibs_i][spec_i])
        fluxes_fibs[fibs_i][spec_i,:] = temp[1].data[7,]
        # Fill wavelength solution matrices
        # wlen_mat_aug[spec_i,:] = temp[4].data[7,]
        # wlen_mat_sep[spec_i,:] = temp[4].data[7,] # THESE ARE TO CHECK ALL WAVELENGTH SOLUTIONS ARE THE SAME IN ONE NIGHT
        temp.close()
        
# EXTRACT HEADER DATA
for spec_i in range(0, n_spectra):
    temp = fits.open(filenames_A[spec_i])
    mjd_obs[spec_i] =   temp[0].header['MJD-OBS']
    airmass[spec_i] =   temp[0].header['AIRMASS']
    hier_bjd[spec_i] =  temp[0].header['HIERARCH CARACAL BJD']
    hier_berv[spec_i] = temp[0].header['HIERARCH CARACAL BERV']
    temp.close()
   
# CHECKS WITH PLOTTING AND PRINTING
# Plot all spectra
for i in range(0, n_spectra):
    plt.plot(wlen_aug[7, ], fluxes_A[i,:]) # Switch letter between B and A as desired.
    
# print(mjd_obs)
# print(filenames_A)

# Change directory to save numpy arrays to a different folder.
os.chdir('C:/Users/Rohan/PycharmProjects/PX402/Spectra arrays');

# np.save('fluxes_A_aug', fluxes_A)    # AUGUST
# np.save('fluxes_B_aug', fluxes_B)
# np.save('mjd_obs_aug', mjd_obs)
# np.save('airmass_aug', airmass)
# np.save('hier_bjd_aug', hier_bjd)
# np.save('hier_berv_aug', hier_berv)

np.save('fluxes_A_sep', fluxes_A)      # SEPTEMBER
np.save('fluxes_B_sep', fluxes_B)
np.save('mjd_obs_sep', mjd_obs)
np.save('airmass_sep', airmass)
np.save('hier_bjd_sep', hier_bjd)
np.save('hier_berv_sep', hier_berv)

# np.save('wlen_soln_aug', wlen_aug[7,])         # WAVELENGTH SOLUTION
# np.save('wlen_soln_sep', wlen_sep[7,]) 
