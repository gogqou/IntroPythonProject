Adhesions runs "process_imgages.py" as its main module

process_images.py should be run from the command line or in an IDE that allows entering arguments. 


example run:
python process_images.py '/home/exampledata/cell1/' cell1 _c .tif '/home/randomdir/csvs/'




                            LONGER EXPLANATION:

This code is setup to process an entire data set of time series images, for each time point of which a stack of size "num" was taken


___________________________Arguments:_____________________________

It takes five arguments:

-## directory ## -- where images should be -- that is, if there are images c1.tif, c2.tif, etc at /home/dir/images/cell1/t1/cell1t1_c1.tif,/home/dir/images/c2.tif..., home_dir = '/home/dir/images/cell1/'


-## dataset ##--which identifies the label for the data set being processed;
	it assumes that there is a naming scheme for each image that includes the dataset name, then the subfolder name under which the image is stored	
	--in our example, dataset = 'cell1'

-## basename ## -- in our example, this would be '_c'; it is whatever identifier might be added onto dataset+subfolder, like NIS elements does when collecting stacks


an optional "## num ##" -- the default is 25 images in the stack

-## heightsdir ## -- directory where a set of csvs, corresponding to each time point, are stored. There's given to where this directory might be because it often happens that we process our adhesion heights in a completely separate workflow. so it's not tied to be under the same home directory as the images themselves. 

__________________Dependencies/Python Packages Needed:___________________________________

numpy
scipy
PIL (Image, matplotlib)

mahotas and pymorph-- available through easy_install or pip, on PyPI 

--these are well documented computer vision libraries 
https://pypi.python.org/pypi/pymorph
https://pypi.python.org/pypi/mahotas/1.0.3


can also be installed from source, see instructions: http://mahotas.readthedocs.org/en/latest/



Python version used: 2.7.3
(as long as it's not Python 3.x, it's fine)
run with EPD (Enthought Python Distribution) v7.3.2--had buffer overflow issues with python2.7 
development done in Ubuntu 12.04 'Precise Pangolin', IDE = Eclipse v3.7.2, pydev through Aptana

__________________Modules:________________________________________

ImageStackgou.py sets up classes Image and ImageStack (with initials at the end for disambiguation), which represent single images and a stack of images, respectively.

*****************************************************************
zproject.py takes a stack of images and "z-projects" them into a single tif image, per ImageJ/FIJI's average intensity algorithm, where all values for a given pixel in a stack are added and averaged over the number of slices in the stack. 
scroll down to 'z project':  http://rsb.info.nih.gov/ij/docs/menus/image.html#stacks 

*****************************************************************
segmentation_watershed.py uses the implementation of the Watershed algorithm in pymorph to identify individual segments (in our case adhesions) in the zprojected image. It applies a Gaussian filter first to smooth out some features. It basically convolves the input signal with the Gaussian distribution and is used to reduce noise. 
See more information: 
http://en.wikipedia.org/wiki/Watershed_%28image_processing%29

http://en.wikipedia.org/wiki/Gaussian_filter and http://docs.scipy.org/doc/scipy-0.7.x/reference/generated/scipy.ndimage.filters.gaussian_filter.html


segmentation_watershed.py returns an ndarray with the same dimensions as the input image. At every location (corresponding to every pixel) there is either a '0' or a number corresponding to which segment the pixel is determined to belong to. 

*****************************************************************
tabulate_adh_props.py compares the output of the segmentation with a heights csv that is formatted the same, but has values corresponding with adhesion protein height--calculated in another program. It populates a new ndarray with height values only at places where there was a height value and a segment number assignment. It also groups segment heights together to calculate the average adhesion height. 

It returns the cross-referenced heights array as well as average adhesion height values and adhesion size (pixel count). 

*****************************************************************

histogram.py plots the average adhesion heights in a histogram and saves it as a .png file in the corresponding time point folder. 


*****************************************************************
draw_segment_image.py labeles each segment with a different color and number so the image can be cross referenced with output csvs with adhesion properties like size and height

*****************************************************************

readcsv.py and readwrite_file.py are utilities that read and write csvs and txt files. 

*****************************************************************

compile_files.py is a utility that goes into a directory and assumes there are two layers of subfolders. It runs through all the files and collects all files that contain a given "keyword" (usually used to identify an extension type) into the topmost folder. 

*****************************************************************


