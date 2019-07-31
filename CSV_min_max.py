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

#1) Read 1 CSV
#2) Get min and max values from that CSV and add that to a list
#3) Close that CSV
#4) Open a new CSV and read
#5) Get min and max values from that CSV and add that to a list
#6) Close that CSV
#7) At end, print min and max values from the min and max lists


#STEVE: think about what we want here. Do we need an entire list?
#		or is just a single minimun and maximum value that is used between
#		each csv?
#
#		Python functions to get the job done:
#		min(num_a, num_b) #returns the minmum to the two inputs
#		max(num_a, num_b) #returns the maximum to the two inputs

#%%
import csv

def csv_min_max(filename):
    f = open(filename, 'r') #open file
#    content = csv.reader(f, delimiter=',')
    for row in csv.reader(f):
        for n in row:
            print(n)
    f.close()

#    with f:
#        content = content[1:] #ignore the first line of the CSV that has the dimensions in it
#        content = csv.reader(f, delimiter=',') #read all the lines in the file
#        min_list = [] #creates a blank list
#        max_list = [] 
#        for row in content:
#            for n in row: #loops through all items in file and adds the minimum value to the list
#                min_list.append(min(n))
#            for n in row:
#                max_list.append(max(n))
#        print(min_list)
#        print(max_list)
#    f.close()
#    
#    print(min(min_list))
#    print(max(max_list))

#%%
