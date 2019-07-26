import converter as cn
import sys
import os

argflag = sys.argv[1]
inname = sys.argv[2]

argMinTemp = None
if len(sys.argv) > 3 :
	argMinTemp = sys.argv[3]

argMaxTemp = None
if len(sys.argv) > 4 :
	argMaxTemp = sys.argv[4]

#single file
if argflag == "-f" :
	cn.csv_to_tiff(inname, argMinTemp, argMaxTemp)

if argflag == "-d" :
	for f in os.listdir(inname) :
		if ".csv" in f :
			cn.csv_to_tiff(inname + "/" + f, argMinTemp, argMaxTemp)
