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
import sys
import os
import json

if len(sys.argv) < 3 :
	print("Invalid arguments: cmd_convert.py <flag> <filename> needed.\n")

args = {}

availableFileTypes = ( 'TIFF', 'PNG' )
args["imageFormat"] = 'TIFF'

createCalibration = False

for i in range(len(sys.argv)) :
	if sys.argv[i] == "-f" :
		args["filename"] = sys.argv[i+1]

	if sys.argv[i] == "-d" :
		args["dir"] = sys.argv[i+1]

	if sys.argv[i] == "-t" and sys.argv[i+1] in availableFileTypes:
		args["imageFormat"] = sys.argv[i+1]

	if sys.argv[i] == "-c":
		print("Calibration Options enabled. Creating calibration images to use for OpenCV.")
		createCalibration = True

print("Converting CSV to {} image format.".format(args["imageFormat"]))

#Read settings from config.json
path = "../bin/config.json"

with open(path) as jsonData :
	data = json.load(jsonData)

currentMin = data["minTemperature"]
currentMax = data["maxTemperature"]

#@TODO find a cleaner way of masking these edge values
#This cutoff value is equal to the cutoff value in mask_creator.py
cutoff = data["maskCutoff"]
    
#single file
if "filename" in args:
	if createCalibration :
		cn.CreateCalibration(args["filename"], filetype=args["imageFormat"])
	else :
		cn.CreateImage(args["filename"], filetype=args["imageFormat"])

#entire directory
if "dir" in args :
	print("Finding min and max temperature range for images...")
	for f in os.listdir(args["dir"]):
		if ".csv" in f :
			current_values = cn.FindMinMax(args["dir"] + "/" + f, currentMin, currentMax, cutoff)
			currentMin = current_values[0]
			currentMax = current_values[1]

	print("Using temperature range [{} - {}]".format(currentMin, currentMax))

	for f in os.listdir(args["dir"]) :
		if ".csv" in f :
			if createCalibration : 
				cn.CreateCalibration(args["dir"] + "/" + f, currentMin, currentMax, filetype=args["imageFormat"])
			else : 
				cn.CreateImage(args["dir"] + "/" + f, currentMin, currentMax, filetype=args["imageFormat"])

print("Image processing complete!")