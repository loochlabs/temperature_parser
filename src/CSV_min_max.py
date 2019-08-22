# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:45:16 2019

@author: kco77
"""

#This script finds the min and max values in a folder of CSV files

#Not sure what the best way to go about this is, but my current plan is to:

#STEVE: before this step, you want to have a directory and read each csv
#		you sort of describe this but I'm adding this to clarify.
#		See lines 13-15 of cmd_converter.py for this

#KC reply to above: I am a bit confused where you put the directory path (see sys.path... that I've added.)
#Do you put it before the function or within the defined function? Because from what I understand python by default
#looks at the current directory. So I need to override that by giving it a directory.
#This is a pretty key thing I need to understand as I will need to do this all the time. (I.e. access files)
#The sys.path.append line I've added, doesn't seem to work. 

#New plan:
#1) Point to a given file directory
#2) Read all the CSVs in that directory
#3) Find the min and max of each CSV
#4) Print the min and max values across all CSVs


#STEVE: think about what we want here. Do we need an entire list?
#		or is just a single minimun and maximum value that is used between
#		each csv?
#
#		Python functions to get the job done:
#		min(num_a, num_b) #returns the minmum to the two inputs
#		max(num_a, num_b) #returns the maximum to the two inputs

#%% current attempt: 

#import numpy as np
import csv
#import sys
#
#sys.path.append("C:\Users\katie\OneDrive - University of Canterbury\My Documents\PhD\Data Analysis\TIR\Test Data") #directory where CSVs are saved

def csv_min_max(filename, current_minimum, current_maximum): #reads file, inputs csv_minimum and csv_maximum variables
    f = open(filename, 'r') #open file
    csv_reader = csv.reader(f)
    
    for row in csv_reader:
        for n in row:
            if float(n) <100:
                current_minimum = min(current_minimum, float(n)) #here we are comparing n to the current_minimum and picking the minimum of the two
                current_maximum = max(current_maximum, float(n)) #here we are comparing n to the current_maximum and picking the maximum of the two
                
    f.close()
    
    return(current_minimum, current_maximum)
