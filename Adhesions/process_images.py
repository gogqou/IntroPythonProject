'''
Created on Dec 4, 2013

@author: gou
'''


import sys
from ImageStackgou import *
import Image
import zproject as zp 
import segmentation_watershed as seg_wt
import readwrite_file as rd_wrt
import tabulate_adh_props as adh_p
import histogram as hist
import os
import compile_files as compilef
import draw_segment_image as draw
import re

def processStack(home_dir, basename, imageext, heightsdir, num = None):
    if num is None:
        num = 25
    #populate the stack based on the provided directory, basename, number of images per stack, and their image extension
    stack=Stack_gou(home_dir, num, basename, imageext)
    #calls zproject to produce an average-intensity value for the stack
    zprojected =  zp.zproject(stack)
    #saves this image
    name =home_dir+basename+'_zprojected'+imageext
    
    plt.imsave(name, zprojected)
    
    #converts zprojected image to greyscale in preparation for segmentation
    image=Image.open(name).convert('L')
    #implements watershed segmentation from the mahotas/pymorph computer vision library
    #*after contrast enhancement and gaussian blurring -- can change
    
    #add option = 'contrast' if want to run contrast enhancement on image before processing
    #otherwise there will only be Gaussian filtering
    print 'about to segment'
    adhesions_array_labels, num_adhesions=seg_wt.segmentation(image, home_dir, basename)
    
    #the output of segmentation is a csv of numbers corresponding with pixels in the original image
    #if a pixel was found to belong to a segment, or adhesion
    #it was a number that groups with all other pixels in that adhesion
    #if not, it will have a value of 0
    rd_wrt.writecsv(adhesions_array_labels,home_dir, 'adhesion_nums.csv')
    heights_array = rd_wrt.readcsv(heightsdir + basename+'H.csv')
    
    #runs compare heights and adhesion segments
    #basically cross-checks between two csvs, one with numbers corresponding to the segmented adhesion number
    #one with heights from imaging data
    #if there is a value for a pixel in both csvs
    #it is recorded and entered into a new array
    #heights for each set of pixels belonging to a segmented adhesion are collected and averaged
    #to find adhesion averaged heights
    #this is saved into adh_avg_heights
    #avg_heights saves all these heights in a list, to be graphed later
    print 'checking heights with segmented adhesions'
    segmented_heights_array, avg_heights, adh_avg_heights, new_adhesions_segment_array = adh_p.comp_heights_segments(adhesions_array_labels, heights_array, minAdh_size=1)
    
    #writes a csv of the heights data that only shows heights where an adhesion was found 
    #in the segmentation
    rd_wrt.writecsv(segmented_heights_array, home_dir, 'segmented_heights.csv')
    
    
    rd_wrt.writecsv(new_adhesions_segment_array, home_dir, 'new_adh_segm.csv')
    
    #writes a csv that has the following columns:
    #adhesion number--based on the segmentation
    #adhesion size (pixel number)
    #height from Scanning Angle Interference Microscopy data
    rd_wrt.writecsv(adh_avg_heights, home_dir, 'avg_heights.csv')
    
    
    #produces a histogram of average adhesion heights
    hist.histogram(avg_heights, home_dir, basename)
    
    csv=rd_wrt.readcsv('new_adh_segm.csv')
    png_output_name = home_dir+basename+'_adhesions'+'.bmp'
    #scalingFactor makes the numbers and adhesions easier to see
    #depends on how big your original image is and how big the segments are
    #try out diff scalingFactors to see result
    #this function also has the option of picking a minimum adhesion size
    #default = 1
    #change by adding minClump = ##, where ## = # pixels 
    draw.makeImage(png_output_name, csv, scalingFactor = 2)
    
def main():
    if len(sys.argv)<6:
        print 'not enough inputs--please enter source directory, data set name, base filename,  image extension, and heights directory\nfor example: "/home/Documents/Images/", cell1, _c, .tif, /home/Documents/Images/'
        sys.exit()
    elif len(sys.argv)>6:
        print 'too many inputs, only used first five'

    home_dir=sys.argv[1] 
    dataset = sys.argv[2]
    basename = sys.argv[3]
    imageext = sys.argv[4]
    heightsdir = sys.argv[5]
    
    folders = os.listdir(home_dir)
    
    #cycles through folders and analyzes each stack within the subfolders
    for folder in folders:
        #practical processes to get the right directory to feed into processStack
        directory = home_dir + folder + '/'
        newbasename = dataset +folder+basename
        new_heightsdir = heightsdir + dataset+'/'+folder+'/'
        print 'processing ' + newbasename + ' in ' + new_heightsdir
        
        processStack(directory, newbasename, imageext, new_heightsdir)
        
        
    #compilef.move(home_dir,'histogram', home_dir)
    
if __name__ == '__main__':
    main()