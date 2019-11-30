'''
find_minmax_for_dataset.py

This script is meant to find the Minimum and Maximum values in all of the CSV data set.
	That min/max value is then written out to config.json.
	This range is used to determine the temperature color range when converting CSV's to TIF.

This script should only need to be run once on the initial data set. The resulting
	Min/max values will be written out to the config file.
'''

from converter import TemperatureParser 
import os
import json

configFilename = "config.json"

with open(configFilename) as jsonData :
	config = json.load(jsonData)

currentMin = config["minTemperature"]
currentMax = config["maxTemperature"]

#@TODO find a cleaner way of masking these edge values
#This cutoff value is equal to the cutoff value in mask_creator.py
cutoff = config["maskCutoff"]

parser = TemperatureParser()

for file in os.listdir(config["datapath"]):
	if ".csv" in file :
		current_values = parser.FindMinMax(config["datapath"] + "/" + file, currentMin, currentMax, cutoff)
		currentMin = current_values[0]
		currentMax = current_values[1]

#Write out the found min/max back to our config.json
config["maxTemperature"] = currentMax
config["minTemperature"] = currentMin

print("Found: Min {}, Max {}".format(currentMin, currentMax))

with open(configFilename, "w") as jsonData:
	jsonData.write(json.dumps(config, ensure_ascii=True, indent=4, sort_keys=True))