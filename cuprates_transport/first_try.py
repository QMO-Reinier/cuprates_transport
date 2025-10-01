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

#%% Calculate the bandstructure

band_s = BandStructure(a_lattice, b_lattice, c_lattice, hopping)

band_s.figMultipleFS2D()

#%%

scat_model = ['isotropic'] # Set the kind of scattering our model has
scat_params = {'gamma_0': 2} # Set the scattering rate in ps^-1

#%%

cond_ob = Conductivity(band_s, mag_field, scattering_models=scat_model,
                       scattering_params=scat_params)

cond_ob.figScatteringColor()
