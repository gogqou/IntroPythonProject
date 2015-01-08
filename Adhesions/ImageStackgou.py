'''
Created on Dec 10, 2013

@author: gou

sets up classes Image_gou and Stack_gou, which represent images and a stack of multiple images from a given folder

stack pulls a set of images, number 1 through stacknum, from a given directory, that all share a "basename" and image_extension

it is initialized with the directory, number of images in the stack, basename, and imageextension


'''
import Image as im
import numpy as np
import matplotlib.pyplot as plt


class Image_gou(object):
    def __init__(self, imagelocation):
        self.directory = imagelocation
        self.name = self.directory
        #import the image pixel information as an numpy array
        #convert L -- greyscale
        self.array = plt.imread(imagelocation, format ='tif')
        self.image = im.open(imagelocation)
        self.size = self.image.size
    def __str__(self):
        return str(self.directory)

    
class Stack_gou(object):
    
    def __init__(self, directory, num, basename, imageext):
        self.directory = directory
        self.stacksize = num
        self.basename = basename
        self.images = []
        
        for i in range(num-1):
            num = str(i+1)
            img = Image_gou(directory+basename+num+imageext)
            self.images.append(img) 
        
    def __str__(self):
        res=[]
        for image in self.images:
                res.append(str(image))
        return '\n'.join(res)
    
    def add_image(self, image):
        #image needs to be an instance of Image_gou
        self.images.append(image)
        
    def access_slice(self, slicenum):
        return self.images[slicenum]
        
        