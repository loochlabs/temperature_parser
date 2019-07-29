#csv to tif
from PIL import Image #PIL is a python package that has the "image" function
import numpy as np
import os.path #Used to grab file directory

#Base RGB color channel [0-255] 
base = 255

# Next three functions are converting temp range to an RGB colour
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

#Main function of interest! 
def csv_to_tiff(filename) : 
	print("Converting {}...".format(filename))

	#read csv convert to an array
	with open(filename) as f : #pass the filename
		content = f.readlines() #reading all the lines in the CSV

	dimensions = content[0] #[0] indicates the first row - so this is grabbing the content from the first row
	dimensions = dimensions.split(",") #this splits the dimensions at the comma - i.e., 382, 288 to 382 and 288
	for n in range(len(dimensions)) :
		dimensions[n] = dimensions[n].strip('\n') #takes out a start new line character from end

	content = content[1:] #disregard dimensions line - splices the array. Content starts at second line (line one and goes to end)

	#create an NxMx3 rgb matrix for each csv entry "N = width, M = height, 3 is the three RGB colour channels
	rgbArray = np.zeros((int(dimensions[1]), int(dimensions[0]), 3), 'uint8') #np.zeros fills the numpy array with zeros
    #dimensions[0] is passing the 382 dimension and dimensions[1] is passing the 288 pixel dimension
    
	#use image mask to remove edge values
	maskFilename = "/../images/mask.png" #name of file
	maskImage = Image.open(os.path.dirname(__file__) + maskFilename) #points to the filepath
	maskImage.load() #loads image
	maskData = np.asarray(maskImage) #creates a mask with the mask image
	maskImage.close()

	#grab all content and store in 1d array of floats (converted to floats below)
	tempMax = 20.5 #float(tempMax) #at the moment, temps are hardcoded, but we can change it to read all csvs and grab the min and max from them
	tempMin = 14.5 #float(tempMin)
	tempDiff = tempMax - tempMin #range of temps in csv

	#set rgb values, apply mask image
	for y in range(len(content)) : #go through each pixel in the csv and assign colour, y = row number
		row = content[y].split(',') #splits each value in the row by the comma
		for x in range(len(row)) : #for each temp value set colour
			#set pixel color based on temperature reading
			rgbArray[y][x][0] = (maskData[y][x][0]/base) * temp_to_r(1 - ((tempMax - float(row[x])) / tempDiff))
			rgbArray[y][x][1] = (maskData[y][x][1]/base) * temp_to_g(1 - ((tempMax - float(row[x])) / tempDiff))
			rgbArray[y][x][2] = (maskData[y][x][2]/base) * temp_to_b(1 - ((tempMax - float(row[x])) / tempDiff))

	#create image file
	im = Image.fromarray(rgbArray)
	outfile = filename.split('.', 1)[0] #strip out old extension name (.csv)
	im.save(outfile + '.tif', 'TIFF') #save it as a tiff and add .tif file name
    