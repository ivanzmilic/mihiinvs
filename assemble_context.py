import numpy as np
import matplotlib.pyplot as plt 
import pyana
import sys
from tqdm import tqdm

path = sys.argv[1]

path = '/dat/milic/MiHi_Fe_I_plage/obs04/context/'

start = 0 
step = 6000

last = 972000

for frame in tqdm(range(start, last, step)):

    fullpath = path+'image.'+str(frame)+'..'+str(frame+step-1)+'.00.00.f0'
    #print(fullpath)
    
    img = pyana.fzread(fullpath)["data"]
    
    if frame == start:
        cube = img

    else :
        cube = np.dstack((cube, img))

print(cube.shape)

Iqs = np.mean(cube)

print (Iqs)

cube /= Iqs

from astropy.io import fits

hdu = fits.PrimaryHDU(cube)
hdul = fits.HDUList([hdu])
hdul.writeto('context_cube.fits', overwrite=True)

# print some cubes

plt.figure(figsize=(10,10))
plt.imshow(cube[:,:,10], origin='lower', cmap='afmhot', vmin=0.5, vmax=1.5)
plt.savefig('context_10.png')
plt.clf()

    