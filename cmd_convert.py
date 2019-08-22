#%%
'''
cmd_convert.py

A script meant to be run from the command line in order to tie together all 
temperature processing functions. 

TODO:
	This can probably be more Windows friendly. Converting this to a batch script might be 
	a better option.

'''

import src.converter as cn
import src.CSV_min_max
import sys
import os

if len(sys.argv) != 3 :
	print("Invalid arguments: cmd_convert.py <flag> <filename> needed.\n")

argflag = sys.argv[1]
inname = sys.argv[2]

#single file
if argflag == "-f" :
	cn.csv_to_image(inname)

currentMin = 100
currentMax = 0
    
if argflag == "-d" :
    for f in os.listdir(inname) :
        if ".csv" in f :
            current_values = cn.findMinMax(inname + "/" + f, currentMin, currentMax)
            currentMin = current_values[0]
            currentMax = current_values[1]

    print("Using temperature range [{} - {}]".format(currentMin, currentMax))

    for f in os.listdir(inname) :
        if ".csv" in f :
            cn.csv_to_image(inname + "/" + f, currentMin, currentMax)