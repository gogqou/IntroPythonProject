'''
Created on Dec 12, 2013

@author: gou
'''
import ImageDraw
import Image
import random
# Create an image from a matrix
# scalingFactor is the scaling factor for the image. For example, 2 will 
# create an image twice as big
# minClumpSize is the minimum size of a group of pixels to draw
def makeImage(imgName, matrix, scalingFactor=1, minClumpSize=1):

    # Get the dimensions of the image from the matrix
    height = len(matrix)
    width = len(matrix[0])
    #print height
    #print width
    
    # Initialize the image with a black background
    img = Image.new('RGB', (scalingFactor*width, scalingFactor*height), 'black')
    
    # This is the object we'll use to draw onto the image
    draw = ImageDraw.Draw(img)
    
    
    # This is a map of all the colors we use
    # For now, we know that 0 (no adhesion) shouldn't be colored
    # We'll fill in this map as we go
    colormap = {0:(0, 0, 0)};
    
    # This is a map that holds that sum of the x-y position of the pixels, 
    # by adhesion value
    # We'll use this later to find the average position of the adhesion
    positions = {}
    
    # This is a map that simply keeps track of how many pixels were in
    # the adhesion.
    # This is also useful for computing the average position, and also
    # deciding whether or not to draw the adhesion.
    val_n = {}
    
    
    
    # Let's first figure out what clumps are there
    
    
    # Iterate over every entry in the matrix
    for x in xrange(height):
        for y in xrange(width):
    
            # This is the value in the image
            val = matrix[x][y]
                       
            
            # We don't care about 0's, so if we have a 0, ignore it and move on
            #if val is 0:
            if val==0:
                #print x,y
                continue
            
            # If we haven't yet assigned a color for this value, do so now
            if not val in colormap:
                # Construct a random RGB color
                # I'm using a baseline of 100 so that we don't draw black
                # pixels, which would be hard to see on a black background
                
                R = 100+random.randint(0, 156)
                G = 100+random.randint(0, 156)
                B = 100+random.randint(0, 156)
                #c = int(255*(val-40)/60.0)
                #color=int(1000*(val-40)/60)
                
                color = (R, G, B)
                #color = (c, c, c)
                
                # Store the color in our color for use later
                colormap[val] = color
            
            # We need to keep track of the positions of all the pixels, so we can know
            # where to draw the text later
            pos = (x, y)
            if val in val_n:
                # If we already came across this value, increment the count
                # and update the sum of the x and y coordinates accordingly
                val_n[val] += 1
    
                # Grab the old position from the map, add in the new position
                # by x and y component, and stick it back in the map
                oldPos = positions[val]
                newPos = ( (pos[0]+oldPos[0]), (pos[1]+oldPos[1]) )
                positions[val] = newPos;
                
        
            else:
                # Otherwise, create the initial entry
                
                # This is the first one, so we only have 1 of this value    
                val_n[val] = 1
                # This is the only position in the map so far, so just stick it in
                positions[val] = pos
            
            
    #print val_n
    #raw_input()
    
    # Now let's go through and actually draw in things
    for x in xrange(height):
        for y in xrange(width):
    
            # Grab the value at this position    
            val = matrix[x][y]
            
            # We'll only draw something if it's nonzero (so, actually an adhesion)
            # and it's bigger than the minimum size we're interested in
            if val!=0 and val_n[val] >= minClumpSize:
            
                # Grab the color we had previously assigned
                color = colormap[val]
                #color = (255,255,255)
                
                # Generate the box, according to the scaling factor
                # ( (top left corner y x), (bottom right corner y x) )
                # y and x are swapped, because that's how they're drawn
                topLeft = (scalingFactor*y, scalingFactor*x) 
                bottomRight = (scalingFactor*(y+1), scalingFactor*(x+1))
                box = (topLeft, bottomRight)
                
                # Now draw the box that represents this matrix entry
                draw.rectangle(box, fill=color)

    # Now let's actually label things
    for val in val_n.keys():
    
        # How many pixels of this value were there?
        n = val_n[val]
        
        # Only label if we had at least the minimum size
        if n > minClumpSize:
            # Compute the average position of all of the pixels we care about
            pos = positions[val]
            avg_pos = ( scalingFactor*pos[0]/n, scalingFactor*pos[1]/n)
            
            # Draw the label, with the text just being the adhesion number, and the
            # position being in the middle of the adhesion itself
            draw.text( (avg_pos[1], avg_pos[0]), str(int(val)))                    
    # Save the image to the given filename
    img.save(imgName, 'BMP')
    return 1

