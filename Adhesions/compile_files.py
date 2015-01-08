'''
Created on Dec 12, 2013

@author: gou
'''


import sys
import shutil
import os

def move(home_dir,keyword, new_dir):
    
    #pulls the filenames of all files and folders within the given directory
    folders = os.listdir(home_dir)
    print folders
    for folder in folders:
        if '.' in folder:
            continue
        else:
            files=os.listdir(home_dir+folder+"/")
            for file in files:
                if keyword in file:
                    current = home_dir+folder+"/"+file
                    new = new_dir+folder+"_"+file
                    #print file
                    shutil.copy(current,new)
    return 1
