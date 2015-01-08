'''
Created on Dec 10, 2013

@author: gou
'''
import numpy as np
def readcsv(filename):
    print filename
    f=open(filename,'rb')
    lines = f.readlines()
    size =[512,512]
    csv_data= np.zeros(size)
    
    #enumerate numbers the lines, the 1 specifies that n starts at 1 instead of 0   
    for n, line in enumerate(lines, 1):
    
        #strips away the \n delimiter at end of each line that makes a new line
        lineagain = line.rstrip()
        #uses ',' as delimiter to separate out the relevant information
        line_split = lineagain.split(',')
        csv_data [n-1,:] = line_split        
   
    return csv_data