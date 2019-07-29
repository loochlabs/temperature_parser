import src.converter as cn
import sys
import os

argflag = sys.argv[1]
inname = sys.argv[2]

#single file
if argflag == "-f" :
	cn.csv_to_image(inname)

if argflag == "-d" :
	for f in os.listdir(inname) :
		if ".csv" in f :
			cn.csv_to_image(inname + "/" + f)
