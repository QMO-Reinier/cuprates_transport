# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 16:34:08 2025

@author: regter
"""

from conductivity import*
from bandstructure import*

#%% Define lattice

# Lattice constants of orhohombric lattice of crystal in Angstrom
a_lattice = 5.5670 
b_lattice = 5.5304
c_lattice = 7.8446

hopping = 100 # in meV

mag_field = 0 # externally applied magnetic field
Temp = 1 # Temperature in Kelvin

#%% Here we define the shape of the sample (rectangle for now)

# Dimensions of channel
width  = 100e-6 
height = 20e-6 

# Convert to grid
nx, ny = 2, 50
dx = width/nx
dy = height/ny
x_array = np.linspace(0, width, nx)
y_array = np.linspace(0, height, ny)
X, Y = np.meshgrid(x_array, y_array)

# Define Scattering profile in ps^-1
gamma_center = 1 
gamma_edge = 50 # More impurities on the edges

#Create quadratic profile
ry = np.minimum(Y, height - Y) / (height/2)   
r  = 1 - ry                                   
gamma_xy = gamma_center + (gamma_edge - gamma_center) * r**2

#%% First define bandstructure object
band_s = BandStructure(a_lattice, b_lattice, c_lattice, hopping)
band_s.runBandStructure()

#%% Calculate conductivity at each pixel

# Define scattering model
scat_model = ['isotropic'] 

cond_tensor_array = np.zeros((nx,ny,3,3)) # at every pixel sigma is a 3 by 3 tensor

for i in range(nx) :
    for j in range(ny):
        '''
        This for loop calculates the 3 by 3 conductivity tensor at each pixel
        '''
        gamma = gamma_xy[j,i]
        scat_params = {'gamma_0': gamma}
        
        cond_ob = Conductivity(band_s, mag_field, scattering_models=scat_model, 
                               scattering_params=scat_params, T=Temp)
        cond_ob.runTransport()
        cond_tensor_array[i,j,:,:] = cond_ob.sigma
        print(f"Lines completed: {j+1}/{ny}")
    print(f"Lines completed: {i+1}/{nx}")


#%%

component = 1, 1  # change to any (m,n)

plt.figure(figsize=(8, 2))  # wide figure for bar shape
# Use pcolormesh to map the 2D array onto X, Y grid
plt.pcolormesh(X*1e6, Y*1e6, cond_tensor_array[:, :, component[0], component[1]].T, 
               shading='auto', cmap='viridis')
plt.colorbar(label=f"sigma[{component[0]+1},{component[1]+1}]")
plt.xlabel("x (um)")
plt.ylabel("y (um)")
plt.gca().set_aspect('auto')  # stretch to match the bar shape
plt.show()