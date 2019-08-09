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

def csv_min_max(filename): #So this should work for reading one file, but what if I want it to read multiple files?
    f = open(filename, 'r') #open file
    csv_reader = csv.reader(f)
    
    min_list = [] #creates a blank list
    max_list = [] 
    for row in csv_reader:
        for n in row: #loops through all items in file and adds the minimum value to the list
            min_list.append(min(n))
        for n in row:
            max_list.append(max(n))
            
    f.close()
    
    print("The min value is: ", min(min_list))
    print("The max value is: ", max(max_list))


#%%
import csv
import sys #think I could also use the os module to achieve the same thing

sys.path.append("C:\Local\OneDrive - University of Canterbury\My Documents\PhD\Data Analysis\TIR\Test Data") #directory where CSVs are saved

def csv_min_max(filename): #At the moment, I seem to only be able to open a specific file, not point to a directory to retrieve the CSV(s)
    f = open(filename, 'r') #open file
    csv_reader = csv.reader(f)

#    next(csv_reader) #ignore the first line of the CSV that has the dimensions in it-do I need this?
    minVal = []
    maxVal = []
    for row in csv_reader:
        minVal.append(row)
        max(row)

    f.close()
    
    print min(row)
    print max(row)

#%% stuff I don't need right now:
    
        min_list = [] #creates a blank list
        max_list = [] 
        for row in array:
            for n in row: #loops through all items in file and adds the minimum value to the list
                min_list.append(min(n))
            for n in row:
                max_list.append(max(n))
        print(min_list)
        print(max_list) 
