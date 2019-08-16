#%%

import src.converter as cn
import sys
import os
import CSV_min_max

argflag = sys.argv[1]
inname = sys.argv[2]

#single file
if argflag == "-f" :
	cn.csv_to_image(inname)

current_minimum = 100
current_maximum = 0
    
if argflag == "-d" :
    for f in os.listdir(inname) :
        if ".csv" in f :
            current_values = CSV_min_max.csv_min_max(inname + "/" + f, current_minimum, current_maximum)
            current_minimum = current_values[0]
            current_maximum = current_values[1]
    print(current_minimum, current_maximum)
    for f in os.listdir(inname) :
        if ".csv" in f :
            cn.csv_to_image(inname + "/" + f)