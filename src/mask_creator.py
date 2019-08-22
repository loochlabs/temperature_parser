'''
Create an image mask from an existing csv
'''

from PIL import Image
import numpy as np

filename = "../data/image_for_mask.csv"

with open(filename) as f :
	content = f.readlines()

dimensions = content[0]
dimensions = dimensions.split(",")
for n in range(len(dimensions)) :
	dimensions[n] = dimensions[n].strip('\n')

content = content[1:]

#set image to 255 (white)
rgbArray = np.full((int(dimensions[1]), int(dimensions[0]), 4), 255, dtype='uint8')

cutoff = 20.5

#set values above the temperature cutoff to 0 (black)
for y in range(len(content)) :
	row = content[y].split(',')
	for x in range(len(row)) :
		if float(row[x]) >= cutoff :
			rgbArray[y][x][0] = 0
			rgbArray[y][x][1] = 0
			rgbArray[y][x][2] = 0
			rgbArray[y][x][3] = 0

#create mask image
im = Image.fromarray(rgbArray)
im.save('../images/mask.png', 'PNG')