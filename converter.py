#csv to tif
from PIL import Image
import numpy as np

def temp_to_b(pct) :
	tmin = 0
	tmid1 = 0.1667
	tmid2 = 0.3333
	tmax = 0.5

	if tmin < pct < tmid1 :
		return int(255*(pct/tmid1)) #[0-255]

	if tmid1 < pct < tmid2 :
		return 255

	if tmid2 < pct < tmax :
		return 255 - int(255*(pct/tmid1)) #[255-0]

	return 0

def temp_to_g(pct) :
	tmin = 0.1667
	tmid1 = 0.3333
	tmid2 = 0.6667
	tmax = 0.8333

	if tmin < pct < tmid1 :
		return int(255*(pct/tmid1)) #[0-255]

	if tmid1 < pct < tmid2 :
		return 255

	if tmid2 < pct < tmax :
		return 255 - int(255*(pct/tmid1)) #[255-0]

	return 0

def temp_to_r(pct) :
	tmin = 0.5
	tmid1 = 0.6667
	tmid2 = 0.8333
	tmax = 1.0

	if tmin < pct < tmid1 :
		return int(255*(pct/tmid1)) #[0-255]

	if tmid1 < pct < tmid2 :
		return 255

	if tmid2 < pct < tmax :
		return 255 - int(255*(pct/tmid1)) #[255-0]

	return 0

def csv_to_tiff(filename, mn, mx) :
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

	#grab all content and store in 1d array of floats
	tempMin = float(mn)
	tempMax = float(mx)
	tempDiff = tempMax - tempMin
	arr = []
	for y in range(len(content)) :
		row = content[y].split(',')
		for x in range(len(row)) :
			if tempMin < float(row[x]) < tempMax : 
				rgbArray[x][y][0] = temp_to_r(1 - ((tempMax - float(row[x])) / tempDiff)) 
				rgbArray[x][y][1] = temp_to_g(1 - ((tempMax - float(row[x])) / tempDiff))  
				rgbArray[x][y][2] = temp_to_b(1 - ((tempMax - float(row[x])) / tempDiff))  

	data32 = np.array(rgbArray)
	np.clip(data32, 0, 255, out=data32)
	data_u8 = data32.astype('uint8')

	im = Image.fromarray(data_u8)

	outfile = filename.split('.', 1)[0]

	im.save(outfile + '.tif', 'TIFF')
