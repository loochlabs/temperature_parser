from converter import TemperatureParser 
import os
import json

configFilename = "config.json"

with open(configFilename) as jsonData :
	config = json.load(jsonData)

parser = TemperatureParser()

for file in os.listdir(config["datapath"]) :
	if ".csv" in file :
		parser.CreateImage(config["datapath"] + "/" + file, config["minTemperature"], config["maxTemperature"])
