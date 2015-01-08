'''
Created on Dec 11, 2013

@author: gou
'''
import numpy as np

import matplotlib.pyplot as plt
import pylab
import matplotlib.path as path
import matplotlib.patches as patches
def histogram(array, directory, basename):
#plot histogram
        fig=plt.figure()
        ax = fig.add_subplot(111)
        
        #we assign the data source (n) and number of bins 
        n,bins = np.histogram(array,50)
        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n
        XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)
        
        # make a patch out of it
        patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
        ax.add_patch(patch)
        
        # update the view limits
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())
        
        #save the image
        pylab.savefig(directory+'histogram'+basename+'.png')