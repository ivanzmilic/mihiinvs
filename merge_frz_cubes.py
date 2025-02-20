import numpy as np 
import matplotlib.pyplot as plt 
import sys
from astropy.io import fits 
import firtez_dz as frz

path = sys.argv[1]
start = 0
N = 48

NP = 9 # tau, T, p, rho, vt, v_z, Bx, By, Bz

cube = 0

for i in range(start,start+N):
	
	temp = frz.read_model("/dat/xenosh/sharing/TimeSeries/"+str(i)+"/Disambiguity/out_out_out_hsra_nx116_ny129_nz64_dz12_ME_Bh.bin")

	if (i == start):
		NX = temp.shape[0]
		NY = temp.shape[1]
		NZ = temp.shape[2]
		cube = np.zeros([N, NP, NX, NY, NZ])

	cube[i,0,:,:,:] = temp.tau[:,:,:]
	cube[i,1,:,:,:] = temp.tem[:,:,:]
	cube[i,2,:,:,:] = temp.pg[:,:,:]
	cube[i,3,:,:,:] = temp.rho[:,:,:]
	cube[i,4,:,:,:] = temp.vmic[:,:,:]
	cube[i,5,:,:,:] = temp.vz[:,:,:]
	cube[i,6,:,:,:] = temp.bx[:,:,:]
	cube[i,7,:,:,:] = temp.by[:,:,:]
	cube[i,8,:,:,:] = temp.bz[:,:,:]

	print("info::time step", i, " done")

kek = fits.PrimaryHDU(cube)
kek.writeto(sys.argv[2], overwrite=True)
	

	
