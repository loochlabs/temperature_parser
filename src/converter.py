#csv to tif
from PIL import Image
import numpy as np
import os.path

def temp_to_b(pct) :
	tmin = 0.25
	tmax = 0.5

	if pct <= tmin :
		return 255

	if tmin < pct <= tmax :
		return 255 - int(255*(pct/tmax)) #[255-0]

	return 0

def temp_to_g(pct) :
	tmin = 0
	tmid1 = 0.25
	tmid2 = 0.75
	tmax = 1.0

	if tmin < pct <= tmid1 :
		return int(255*(pct/tmid1)) #[0-255]

	if tmid1 < pct <= tmid2 :
		return 255

	if tmid2 < pct <= tmax :
		return 255 - int(255*(pct/tmax)) #[255-0]

	return 0

def temp_to_r(pct) :
	tmin = 0.5
	tmid = 0.75

	if tmin < pct <= tmid :
		return int(255*(pct/tmid)) #[0-255]

	if tmid < pct :
		return 255

	return 0

def csv_to_tiff(filename) :
	print("Converting {}...".format(filename))

	with open(filename) as f :
		content = f.readlines()

	dimensions = content[0]
	dimensions = dimensions.split(",")
	for n in range(len(dimensions)) :
		dimensions[n] = dimensions[n].strip('\n')

	content = content[1:]
	contentArr = []

	#create an NxMx3 rgb matrix for each csv entry
	rgbArray = np.zeros((int(dimensions[0]), int(dimensions[1]), 3), 'uint8')

	#use image mask to remove edge values
	maskFilename = "/../images/mask.png"
	maskImage = Image.open(os.path.dirname(__file__) + maskFilename)
	maskImage.load()
	maskData = np.asarray(maskImage)
	maskImage.close()

	#TODO process all csvs before hand to get these values
	#find min/max temperature in this file
	'''
	tempMin = float(1000)
	for y in range(len(content)) :
		row = content[y].split(',')
		for x in range(len(row)) :
			tempMin = min(tempMin, float(row[x]))

	tempMax = float(-1000)
	for y in range(len(content)) :
		row = content[y].split(',')
		for x in range(len(row)) :
			tempMax = max(tempMax, float(row[x]))
	'''
	#grab all content and store in 1d array of floats
	tempMax = 20.5 #float(tempMax)
	tempMin = 14.5 #float(tempMin)
	tempDiff = tempMax - tempMin

	#set rgb values, apply mask image
	for y in range(len(content)) :
		row = content[y].split(',')
		for x in range(len(row)) :
			#if tempMin < float(row[x]) < tempMax : 
			rgbArray[x][y][0] = (maskData[x][y][0]/255) * temp_to_r(1 - ((tempMax - float(row[x])) / tempDiff)) 
			rgbArray[x][y][1] = (maskData[x][y][1]/255) * temp_to_g(1 - ((tempMax - float(row[x])) / tempDiff))  
			rgbArray[x][y][2] = (maskData[x][y][2]/255) * temp_to_b(1 - ((tempMax - float(row[x])) / tempDiff))  

	#create image file
	im = Image.fromarray(rgbArray)
	outfile = filename.split('.', 1)[0]
	im.save(outfile + '.tif', 'TIFF')
