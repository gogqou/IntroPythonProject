'''
Created on Dec 11, 2013

@author: gou
'''
import numpy as np
def comp_heights_segments(segment_array, heights_array, minAdh_size=5):
    size = [512, 512]
    row = size[0]
    column = size[1]
    new_adhesions_segment_array = np.zeros(size)
    segmented_heights_array = np.zeros(size)
    adhesion_array = np.zeros([180000,4])
    #cycle through the segment array and if the value is not zero, go to the 
        #heights csv at the same position, and populate the segmented_heights array with that number
    adh_row=0
   
    for k in range(row):
        for j in range(column):
            rownum=k
            colnum=j
            if segment_array[rownum,colnum]>0 and heights_array[rownum,colnum]>0:
                segmented_heights_array[rownum,colnum] = heights_array [rownum,colnum]
                new_adhesions_segment_array[rownum, colnum]=segment_array[rownum,colnum]
                #print 'row '+str(rownum+1) +' column ' + str(colnum+1)
                
                #also populate the 4 column array with adhesion number, row number, column number
                #print rownum, colnum
                adhesion_array[adh_row,0] = segment_array[rownum,colnum]
                adhesion_array[adh_row,1] = rownum+1
                adhesion_array[adh_row,2] = colnum+1
                adhesion_array[adh_row,3] = segmented_heights_array[rownum,colnum]
                
                #increment the row of the adhesion_array that we will be writing to
                adh_row+=1
            else:
                continue  
    adhesion_array = adhesion_array[0:adh_row]
    
    #pull out the unique adhesions by number using the separate_adhesions function
    adh_nums= separate_adhesions(adhesion_array,0)
    
    #creates key for adhesion number to number of pixels in adhesion
    adh_pixel_count = {}
    
    #creates key for adhesion number to sum of all pixel heights
    adh_total_height = {}
    
    #creates key for adhesion number to average height
    adh_avg_heights = {}
    
    row_count = -1
    
    #allocate space that will later be populated with the average heights of each adhesion
    #there are two lists/arrays because the avg_heights list will be used to generate the histogram
    #the array will be used to output a csv, and is the repository for the more complete information
    #it includes pixel count and average height for each adhesion number
    adh_avg_heights_array = np.zeros([len(adh_nums),3])
    avg_heights =np.zeros([len(adh_nums),1])
    
    
    #cycle through each adhesion number in the unique list we created
    for adh in adh_nums:
                    
        for m in range(adh_row):
            
            #to deal with the way python treats arrays, we have to pull out each row separately
            #in order to access individual entries within the row
            #so we cycle through each row individually
            
            adhesion_row = adhesion_array[m]
            
            #first we compare the first value to our adhesion number of interest
            #if they're not the same, we move on
            if adhesion_row[0]!=adh:
                continue
            
            #if the adhesion number is the same as the adhesion number of the row (first entry)
            else:
                
                # if there's already a mapping for this adhesion number
                if adh in adh_pixel_count:
                    
                    #increment pixel count for the adhesion
                    adh_pixel_count[adh]+=1
                    
                    #pull old height number
                    adh_height_total_old = adh_total_height[adh]
                    adh_height_total_new = adh_height_total_old+ adhesion_row[3]
                    adh_total_height[adh]=adh_height_total_new
                
                #if there isn't a mapping for this adhesion number to pixel count, which means
                #it's the first time we're encountering it
                
                else: 
                    
                    #we initialize each mapping
                    adh_pixel_count[adh]=1
                    #the total height is just the height of this one adhesion, which is the fourth entry in the row
                    #(recall that the row goes: adhesion number, x,y, height)
                    adh_total_height[adh]=adhesion_row[3]
                    
        #we assign the pixel count and total height values so we can operate on them later
        pixel_count = adh_pixel_count[adh]
        total_height = adh_total_height[adh]
        
        #use pixel count and heights sum to calculate average height
        adh_avg_heights[adh]=total_height/pixel_count
        
        #we set a minimum adhesion size, based on pixel count
        #this is defined in the input of this function, and is hard coded in right now
        if adh_pixel_count[adh]>=minAdh_size:
            #we're keeping track of how many adhesions pass this cutoff
            row_count +=1
            
            #populating the average heights lists/arrays
            
            #each array row goes: adhesion number, pixel count, average height of pixels in adhesion
            adh_avg_heights_array [row_count]= [adh, adh_pixel_count[adh],adh_avg_heights[adh]]
            #the list is just the average adhesion heights in ascending order of the adhesion number
            avg_heights[row_count]=[adh_avg_heights[adh]]
            
            
    adh_avg_heights_array=adh_avg_heights_array[0:row_count]
    avg_heights = avg_heights[0:row_count]
    #print adh_avg_heights_array
    return segmented_heights_array, avg_heights, adh_avg_heights_array,new_adhesions_segment_array
def separate_adhesions(array,index):
    #need to hard code the pattern
    
    #pulling out all the unique adhesion numbers within the adhesion array
    s=set([e[index] for e in array])
    adh_nums= []
    
    for adh_num in s:
        adh_nums=adh_nums + [adh_num]
    #sorts from smallest to largest
    adh_nums.sort()
       
    return adh_nums

