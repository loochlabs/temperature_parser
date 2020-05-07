from converter import TemperatureParser 
import os
import json
import csv

configFilename = "../config.json"

with open(configFilename) as jsonData :
	config = json.load(jsonData)

currentMin = config["minTemperature"]
currentMax = config["maxTemperature"]

filename = config["LegendFileName"]
imageWidth = int(config["LegendWidth"])
imageHeight = int(config["LegendHeight"])

dt = currentMax - currentMin

legendcsv = open(filename, "w")
#content = []
#content.append()
legendcsv.write(str("{},{}\n".format(imageWidth, imageHeight)))

#fill a fake temperature array with our color range
#go from [0-100]%, generate a temperature 
rowWidth = int(float(imageWidth) / 100)
for h in range(imageHeight) :
	row = ""
	for n in range(100) :
		value = currentMin + (dt * (float(n)/100))
		row += ("{},".format(value) * rowWidth)
	#content.append(row)
	legendcsv.write(row[:-1] + "\n")

legendcsv.close()

parser = TemperatureParser()
parser.CreateImageFromFile(filename, currentMin, currentMax, 'PNG', False)