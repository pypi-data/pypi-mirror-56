#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:23:15 2019

@author: mpolikarpov
"""
import os
os.environ['OMP_NUM_THREADS'] ='1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

from maximus48 import var
import numpy as np
from multiprocessing import Array
from maximus48.multiCTF2 import shift_distance as shift
 
"""
some functions here are out of classes - if you compare to the file tomo_proc.py
the reason for that - I wanted to make clases F and Processor as light as possible
 for parallel processing 
so, in a sence, I use them almost as fast dictionaries
"""

# =============================================================================
# tomo-functions
# =============================================================================

def tonumpyarray(shared_array, shape, dtype):
    '''Create numpy array from shared memory.'''
    nparray = np.frombuffer(shared_array, dtype=dtype).reshape(shape)    
    #assert nparray.base is shared_array
    return nparray
        

def correct_shifts(shifts, median_dev = 5):
    """find any bad numbers which are deviate more than 5 pixels from the median
    and correct them to median of the array"""
    
    shifts = tonumpyarray(shifts.shared_array_base, shifts.shape, shifts.dtype)
    
    for i in range(shifts.shape[1]):
        for j in range(shifts.shape[2]):
            shifts[:,i,j] = np.where((abs(shifts[:,i,j] - np.median(shifts[:,i,j])) > median_dev), np.median(shifts[:,i,j]), shifts[:,i,j])
    print('adjusted shifts') 


def rotaxis(proj, N_steps, ROI_ff = None):
    """calculate the rotation axis comparing 0 and 180 projection shift
    proj: 3D array
    N_steps: projections per degree
    N_rot: number of files that have their mirrors
    ROI_ff: where to make comparison
    
    """
    if not ROI_ff:
        ROI_ff = 0,0, proj.shape[1], proj.shape[0]
        
    cent = []
    N_rot = proj.shape[0] - 180 * N_steps
    
    for i in range(N_rot):
        distances = shift(proj[i, ROI_ff[1]:ROI_ff[3], ROI_ff[0]:ROI_ff[2]], 
              np.flip(proj[i + N_steps*180, ROI_ff[1]:ROI_ff[3], ROI_ff[0]:ROI_ff[2]] ,1))
        cent.append(proj[i].shape[1]/2 + distances[1]/2)
    return cent
    

        

# =============================================================================
# #actually should be a part of the Processor class - check tomo_proc.py
# =============================================================================

def init_Npad(ROI, compression = 8):
    """Calculate the Npad for padding
    can be adjusted with compression parameter
    By default, 8 times smaller than ROI
    """
                    
    if (ROI[2]-ROI[0])>(ROI[3]-ROI[1]):
        Npad = (ROI[2]-ROI[0])//compression       
    else:
        Npad = (ROI[3]-ROI[1])//compression   
        
    return Npad 


def init_names(data_name, N_distances, first_distance = 1):
    """set proper data_names"""
    
    data_names = []
    ff_names = []
    
    for i in range(first_distance, N_distances + first_distance):
        data_names.append(data_name + '_' + str(i))
        ff_names.append('ff_' + data_name + '_' + str(i))
        
    return data_names, ff_names 







# =============================================================================
# classes themselves
# =============================================================================
class Processor:
    __slots__ = ['ROI', 'ROI_ff', 'Npad', 'im_shape', 'images', 'flats',
                 'N_files', 'N_start']
        
    def __init__(self, ROI, folder, N_start, N_finish, compNpad = 8):
        """Initialize parameters. 
        Normally should contain ROI, N_distances, etc
        """
        self.N_start = N_start
        self.ROI = ROI
        self.N_files = (N_finish - N_start) 
        self.im_shape = (ROI[3]-ROI[1], ROI[2]-ROI[0])  
        self.Npad = init_Npad(ROI, compression = compNpad)
        
        
    def init_paths(self, data_name, path, N_distances):
        """Generate paths images & flatfields"""
    
        #set data_names
        data_names, ff_names = init_names(data_name, N_distances)
        
        #find images
        imlist = var.im_folder(path)
        
        #set proper paths
        images = np.zeros(N_distances, 'object') 
        flats = np.zeros(N_distances, 'object')
                
        for i in np.arange(len(images)):
            #sort image paths
            images[i] = [path+im for im in imlist if (im.startswith(data_names[i])) and not (im.startswith('.'))]
            flats[i] = [path+im for im in imlist if im.startswith(ff_names[i])]
            
        self.images = images
        self.flats = flats

                        

class F:
    __slots__ = ['shape', 'dtype', 'shared_array_base']
    
    def __init__(self, shape, dtype = 'd'):
        """Create shared value array for processing.
        """
        self.shape = shape
        self.dtype = dtype
        
        ncell = int(np.prod(self.shape))
        self.shared_array_base = Array(dtype, ncell,lock=False)       
        pass
     
        
    

