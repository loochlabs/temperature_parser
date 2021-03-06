'''
converter.py

Description: Primary utility functions for converting csv temperature data to images.
'''

from PIL import Image 
import numpy as np
import os.path 
import csv
import json

class TemperatureParser :

	#Global Base RGB color channel [0-255] 
	base = 255
	maskData = []

	config = {}
	configFilename = "../config.json"

	def __init__(self) :
		#use image mask to remove edge values
		with open(self.configFilename) as jsonData :
			self.config = json.load(jsonData)

		maskFilename = self.config["maskFilename"] #name of file
		maskImage = Image.open(maskFilename)
		maskImage.load() 
		self.maskData = np.asarray(maskImage) 
		maskImage.close()

	'''
	findMinMax

	Description: Find the min and max temperature in a csv file in a single pass. 
		Typically this is going to be used to process a batch of csv files, hence the extra
		min and max params.
	Params:
		filename : csv file of temperatures
		currentMin : minimum temp found in previous calls
		currentMax : maximum temp found in previous calls
		cutoff : This is the top range of our temperatures. Images have a rim of warm temperature
			readings that we want to throw away. See mask_creator.py for more details. 
	'''
	def FindMinMax(self, filename, currentMin, currentMax, cutoff): 
		f = open(filename, 'r') 
		csv_reader = csv.reader(f)

		for row in csv_reader:
			for n in row:
				currentMin = min(currentMin, float(n)) 

				if float(n) < cutoff:
					currentMax = max(currentMax, float(n)) 
	                
		f.close()
	    
		return (currentMin, currentMax)


	# Next three functions are converting temp range to an RGB colour
	def temp_to_b(self,pct) :
		tmin = 0.5
		tmax = 0.67

		if pct <= tmin :
			return self.base

		if tmin < pct and pct <= tmax :
			trange = tmax - tmin
			tdiff = tmax - pct
			tpct = 1 - (float(tdiff/trange))
			return self.base - int(self.base*tpct) #[255-0]

		if pct > 1 :
			return self.base

		return 0

	def temp_to_g(self,pct) :
		tmin = 0
		tmid1 = 0.50
		tmid2 = 0.83
		tmax = 1.0

		if tmin < pct and pct <= tmid1 :
			trange = tmid1 - tmin
			tdiff = tmid1 - pct
			tpct = 1 - (float(tdiff/trange))
			return int(self.base*tpct) #[0-255]

		if tmid1 < pct and pct <= tmid2 :
			return self.base

		if tmid2 < pct and pct <= tmax :
			trange = tmax - tmid2
			tdiff = tmax - pct
			tpct = 1 - (float(tdiff/trange))
			return self.base - int(self.base*tpct) #[255-0]

		if pct > 1 :
			return self.base

		return 0

	def temp_to_r(self,pct) :
		tmin = 0.67
		tmid = 0.83
		tmax = 1.0

		if tmin < pct and pct <= tmid :
			trange = tmid - tmin
			tdiff = tmid - pct
			tpct = 1 - (float(tdiff/trange))
			return int(self.base*tpct) #[0-255]

		if tmid < pct and pct <= tmax:
			return self.base

		if pct > 1 :
			return self.base

		return 0


	def CreateCalibration(self, filename, minTemp=0, maxTemp=100, filetype="TIFF") : 
		print("	Creating calibration image: {}".format(filename))

		#read csv convert to an array
		with open(filename) as f : 
			content = f.readlines() 

		dimensions = content[0] 
		dimensions = dimensions.split(",")
		for n in range(len(dimensions)) :
			dimensions[n] = dimensions[n].strip('\n') 

		#fallback on csv dimensions
		if(len(dimensions) != 2) :
			dimensions = []
			dimensions.append(382)
			dimensions.append(288)

		content = content[1:] 

		#create an NxMx3 rgb matrix for each csv entry "N = width, M = height, 3 is the three RGB colour channels
		rgbArray = np.zeros((int(dimensions[1]), int(dimensions[0]), 4), 'uint8') 

		#Simple Mask
		#negative values will be written out as BLACK
		#positive values will be written out as WHITE
		for y in range(len(content)) : 
			row = content[y].split(',') 
			for x in range(len(row)) : 
				pixel = 0
				if float(row[x]) < 0.0 :
					pixel = 255

				rgbArray[y][x][0] = pixel
				rgbArray[y][x][1] = pixel
				rgbArray[y][x][2] = pixel

				#alpha channel
				rgbArray[y][x][3] = 255

		#create image file
		im = Image.fromarray(rgbArray)
		outfile = filename.split('.', 1)[0] 
		filetypeExt = { 'TIFF': ".tif", 'PNG': '.png' }
		im.save(outfile + "_grey" + filetypeExt[filetype], filetype) 


	def CreateImage(self, filename, content, minTemp, maxTemp, filetype, useMask=True) :
		dimensions = content[0] 
		dimensions = dimensions.split(",") 
		for n in range(len(dimensions)) :
			dimensions[n] = dimensions[n].strip('\n') 

		#fallback on csv dimensions
		if(len(dimensions) != 2) :
			dimensions = []
			dimensions.append(382)
			dimensions.append(288)

		#disregard dimensions line - splices the array. Content starts at second line (line one and goes to end)
		content = content[1:] 

		#create an NxMx3 rgb matrix for each csv entry "N = width, M = height, 3 is the three RGB colour channels
	    #dimensions[0] is passing the 382 dimension and dimensions[1] is passing the 288 pixel dimension
		rgbArray = np.zeros((int(dimensions[1]), int(dimensions[0]), 4), 'uint8') 
	    
		#grab all content and store in 1d array of floats (converted to floats below)
		tempMax = float(maxTemp) 
		tempMin = float(minTemp) 
		tempDiff = tempMax - tempMin 

		#set rgb values, apply mask image
		#go through each pixel in the csv and assign colour, y = row number
		mask = [255,255,255]
		for y in range(len(content)) : 
			row = content[y].split(',') 
			for x in range(len(row)) : 
				percent = 1 - ((tempMax - float(row[x])) / tempDiff)

				rgbArray[y][x][3] = 255
				if useMask :
					mask[0] = self.maskData[y][x][0]
					mask[1] = self.maskData[y][x][1]
					mask[2] = self.maskData[y][x][2]

					#alpha channel
					rgbArray[y][x][3] = self.maskData[y][x][3]

				rgbArray[y][x][0] = int(mask[0]/self.base) * self.temp_to_r(percent)
				rgbArray[y][x][1] = int(mask[1]/self.base) * self.temp_to_g(percent)
				rgbArray[y][x][2] = int(mask[2]/self.base) * self.temp_to_b(percent)
				
		#create image file
		im = Image.fromarray(rgbArray)
		filetypeExt = { 'TIFF': ".tif", 'PNG': '.png' }
		outname = filename.replace(".csv", filetypeExt[filetype])
		im.save(outname, filetype) 

	'''
	csv_to_image

	Destription: @TODO
	Params: @TODO
	'''
	def CreateImageFromFile(self, filename, minTemp=0, maxTemp=100, filetype="TIFF", useMask=True) : 
		print("	Converting {}".format(filename))

		#read csv convert to an array
		with open(filename) as f : 
			content = f.readlines() 

		self.CreateImage(filename, content, minTemp, maxTemp, filetype, useMask)
		

	def CreateImages(self) :
		for file in os.listdir(self.config["datapath"]) :
			if ".csv" in file :
				self.CreateImageFromFile(self.config["datapath"] + "/" + file, self.config["minTemperature"], self.config["maxTemperature"])

		    