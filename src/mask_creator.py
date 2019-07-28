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

rgbArray = np.full((int(dimensions[0]), int(dimensions[1]), 3), 255, dtype='uint8')

cutoff = 20.5

for y in range(len(content)) :
	row = content[y].split(',')
	for x in range(len(row)) :
		if float(row[x]) >= cutoff :
			rgbArray[x][y][0] = 0
			rgbArray[x][y][1] = 0
			rgbArray[x][y][2] = 0

#create mask image
im = Image.fromarray(rgbArray)
im.save('../data/mask.png', 'PNG')