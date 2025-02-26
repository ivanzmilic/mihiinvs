import numpy as np 
import matplotlib.pyplot as plt 
from astropy.io import fits 
import firtez_dz as frz
import sys

input_pm_atm = sys.argv[1]



atmos_in_filename = sys.argv[1]

atmos_me = fits.open(atmos_in_filename)[0].data
print ("info::the shape of the input ME atmosphere is: ", atmos_me.shape)

# We could start from the time-dependent case but we already have PM inversions in the folder
#snapshot_no = int(sys.argv[2]) # this is the number of the binned snapshot for firtez

# average over the three neigboring ones:
#atmos_me_t = np.mean(atmos_me[snapshot_no:snapshot_no+3,:,:,:], axis=0)

# What are we starting from? Let's say we start from a 3D atmosphere that GJ already prepared

# load that atmosphere:

atmos_in_frz_filename = sys.argv[2]

atmos_frz = frz.read_model(atmos_in_frz_filename)
print ("info::the shape of the input FRZ atmosphere is: ", atmos_frz.tem.shape)

# find the Bx, By, Bz of the ME atmosphere:
Bx_me = atmos_me[:,:,0] * np.sin(atmos_me[:,:,1]) * np.cos(atmos_me[:,:,2])
By_me = atmos_me[:,:,0] * np.sin(atmos_me[:,:,1]) * np.sin(atmos_me[:,:,2])
Bz_me = atmos_me[:,:,0] * np.cos(atmos_me[:,:,1])

atmos_frz.bx[:,:,:] = Bx_me[:,:,None]
atmos_frz.by[:,:,:] = By_me[:,:,None]
atmos_frz.bz[:,:,:] = Bz_me[:,:,None]


atmos_frz.vz[:,:,:] = atmos_me[:,:,3][:,:,None] * 1E5 
# We could, in principle initialize temperature better too. 

atmos_frz.write_model(atmos_in_frz_filename[:-4]+'_me_init.bin')





