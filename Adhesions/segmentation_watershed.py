'''
Created on Dec 11, 2013

@author: gou
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import pylab
import Image 
import mahotas
import ImageEnhance
import pymorph

def segmentation(image, directory, basename, option = None):
    if option != None:
        
        image=ImageEnhance.Contrast(image)
        image=image.enhance(1.5)
        #enhance contrast by 50%
        
        #save enhanced image for calling as array later
        image.save(directory+basename+'_zprojected_enhanced.tif')
        image=mahotas.imread(directory+basename+'_zprojected_enhanced.tif')
    else:
        image = image
    #gaussian filter based on sigma (secondar argument), standard deviation of surrounding pixels
    imagef = ndimage.gaussian_filter(image, 3)
    #OTSU thresholding --cluster based thresholding; minimizes intra-class variance and maximizes inter-class variance
    #between groups of objects
    #binarizes
    T = mahotas.thresholding.otsu(imagef)
    #count distinct objects in binarized image
    labeled,nr_objects = ndimage.label(imagef > T)
    
    #generate seeds for Watershed algorithm
    rmax = pymorph.regmax(imagef)
    seeds, nr_adhesion = ndimage.label(rmax)
    
   
    #applies distance transform to thresholded image
    #the distance transform labels each pixel with its distance from the nearest "obstacle"
    #in a binary image, this would be a boundary pixel where the values change from 0 to 1 or vice versa
    dist=ndimage.distance_transform_edt(imagef>T)
    dist = dist.max()-dist
    dist-=dist.min()
    dist = dist/float(dist.ptp())*255
    dist = dist.astype(np.uint8)
    
    
    adhesions = pymorph.cwatershed(dist,seeds)
    #pylab.imshow(adhesions)
    #pylab.show()
    #clears the memory of the opened figure, so for large data sets, you don't run out
    plt.close()
    return adhesions, np.amax(adhesions)


