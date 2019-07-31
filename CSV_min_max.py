# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:45:16 2019

@author: kco77
"""

#This script finds the min and max values in a folder of CSV files

#Not sure what the best way to go about this is, but my current plan is to:
#1) Read 1 CSV
#2) Get min and max values from that CSV and add that to a list
#3) Close that CSV
#4) Open a new CSV and read
#5) Get min and max values from that CSV and add that to a list
#6) Close that CSV
#7) At end, print min and max values from the min and max lists

import csv 
#import numpy as np #not sure yet if I need numpy
#import sys #do I need this? 

def csv_min_max(filename):
    f = open('Ellesmere_IR_flight01_1000ft_000028.csv', 'r') #open file

    with f: 
        content = content[1:] #ignore the first line of the CSV that has the dimensions in it
        content = csv.reader(f, delimiter=',') #read all the lines in the file
        min_list = [] #creates a blank list
        max_list = [] 
        for row in content:
            for n in row: #loops through all items in file and adds the minimum value to the list
                min_list.append(min(n))
            for n in row:
                max_list.append(max(n))
        print(min_list)
        print(max_list)
    f.close()
    
    print(min(min_list))
    print(max(max_list))
    