'''
Created on Dec 10, 2013

@author: gou
'''
import numpy as np
import scipy
import Image
import math
from scipy import stats
from ImageStackgou import *

def zproject(stack):
    
    size = stack.stacksize
    img=stack.access_slice(14)
    img_dim1 = int(img.size[0])
    img_dim2 = int(img.size[1])
    sum_array = np.zeros([img_dim1, img_dim2])
    
    for i in range(size-1):
        img = stack.access_slice(i)
        array = img.array
        sum_array = np.add(sum_array,array)
        i=+1
    averaged_array = sum_array/size
    #averaged_array= averaged_array.astype('uint8')
    return averaged_array
