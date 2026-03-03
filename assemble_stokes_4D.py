import numpy as np
import matplotlib.pyplot as plt 
#import pyana
import sys
from tqdm import tqdm
from astropy.io import fits


path = sys.argv[1]

#path = '/dat/milic/MiHi_Fe_I_plage/obs04/context/'
#path = '/dat/milic/Na_MiHI/plage/obs01/mihi_sp/lr0500/'

start = 0 
step = 1600 # This is amount of frames in one cube.
            # if you need time, typically there is 600 frames per second.

last = 1537600
#last = start + 5*step
#last = start + 5*2*step

for frame in tqdm(range(start, last, step)):

    # For Carlos, we want average of the two cubes.
    '''
    fullpath = path+'img_fit.'+str(frame)+'..'+str(frame+step)+'.00.00.lr0500.cube.fits'
    stokes1 = fits.open(fullpath)[0].data[10:-10,10:-10,:,300:460]
    ll1 = fits.open(fullpath)[1].data[300:460]
    fullpath = path+'img_fit.'+str(frame+step)+'..'+str(frame+2*step)+'.00.00.lr0500.cube.fits'
    stokes2 = fits.open(fullpath)[0].data[10:-10,10:-10,:,300:460]
    ll2 = fits.open(fullpath)[1].data[300:460]
    stokes = (stokes1 + stokes2) * 0.5
    ll = (ll1 + ll2) * 0.5

    stokes = stokes.reshape(1, stokes.shape[0], stokes.shape[1], stokes.shape[2],-1)
    ll = ll.reshape(1, ll.shape[0])
    '''

    # But for Cori, we want full resolution cubes, and we will only do Stokes I and V, also clean up wavelengths a bit.
    
    fullpath = path+'img_fit.'+str(frame)+'..'+str(frame+step)+'.00.00.lr0500.cube.fits'
    
    stokes = fits.open(fullpath)[0].data[12:-12,12:-12,[0,3],35:475]
    ll = fits.open(fullpath)[1].data[35:475]
    stokes = stokes.reshape(1, stokes.shape[0], stokes.shape[1], stokes.shape[2],-1)
    
    
    if frame == start:
        cube = stokes
        llseries = ll

    # but these are now 4D cubes, so we need to stack along a new axis
    else :
        cube = np.concatenate((cube, stokes), axis=0)
        #llseries = np.concatenate((llseries, ll), axis=0)

print(cube.shape)
print(llseries.shape)

hdu = fits.PrimaryHDU(cube)
# Add some header information here:
hdu.header['XSTEP'] = 0.059 # step in arcseconds
hdu.header['YSTEP'] = 0.059 # step in arcseconds
hdu.header['TSTEP'] = step/600.0 # timestep in seconds, assuming 600 frames per second

hdu1 = fits.ImageHDU(llseries)
hdul = fits.HDUList([hdu, hdu1])
hdul.writeto(path+'cubeseries_Na_cori.fits', overwrite=True)
