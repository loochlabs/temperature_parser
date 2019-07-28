#csv to tif
from PIL import Image
import numpy as np
import os.path

#Base RGB color channel [0-255]
base = 255

#Desaturation factor
#TODO soft code this in config file
desaturation = 0.3

def temp_to_b(pct) :
	tmin = 0.25
	tmax = 0.5

	if pct <= tmin :
		return base

	if tmin < pct <= tmax :
		return base - int(base*(pct/tmax)) #[255-0]

	return 0

def temp_to_g(pct) :
	tmin = 0
	tmid1 = 0.25
	tmid2 = 0.75
	tmax = 1.0

	if tmin < pct <= tmid1 :
		return int(base*(pct/tmid1)) #[0-255]

	if tmid1 < pct <= tmid2 :
		return base

	if tmid2 < pct <= tmax :
		return base - int(base*(pct/tmax)) #[255-0]

	return 0

def temp_to_r(pct) :
	tmin = 0.5
	tmid = 0.75

	if tmin < pct <= tmid :
		return int(base*(pct/tmid)) #[0-255]

	if tmid < pct :
		return base

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

	#grab all content and store in 1d array of floats
	tempMax = 20.5 #float(tempMax)
	tempMin = 14.5 #float(tempMin)
	tempDiff = tempMax - tempMin

	#set rgb values, apply mask image
	for y in range(len(content)) :
		row = content[y].split(',')
		for x in range(len(row)) :
			#set pixel color based on temperature reading
			rgbArray[x][y][0] = (maskData[x][y][0]/base) * temp_to_r(1 - ((tempMax - float(row[x])) / tempDiff))
			rgbArray[x][y][1] = (maskData[x][y][1]/base) * temp_to_g(1 - ((tempMax - float(row[x])) / tempDiff))
			rgbArray[x][y][2] = (maskData[x][y][2]/base) * temp_to_b(1 - ((tempMax - float(row[x])) / tempDiff))

			#desaturation channel if we want to soften these colors
			rgbArray[x][y][0] += ((base-rgbArray[x][y][0]) *desaturation)
			rgbArray[x][y][1] += ((base-rgbArray[x][y][1]) *desaturation)
			rgbArray[x][y][2] += ((base-rgbArray[x][y][2]) *desaturation)

	#create image file
	im = Image.fromarray(rgbArray)
	outfile = filename.split('.', 1)[0]
	im.save(outfile + '.tif', 'TIFF')
