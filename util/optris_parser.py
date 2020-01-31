# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:22:49 2019

@author: kco77
"""

#%% Script for extracting GPS data from Optris files and writing to a CSV

import csv
import os
import json

#enter file directory here where Optris files are saved
configFilename = "../config.json"
with open(configFilename) as jsonData :
    config = json.load(jsonData)

#create a list of the data for the CSV
csv_list = []

def read_optris(filename) :    
    #these are the items that go in the list to fill the csv    
    outputName = filename.split("/")[-1].replace(".optris", ".tif")
    defaultReturn = {"Filename":outputName, "Latitude":"NaN", "Longitude":"NaN", "Altitude":304.8}

    #open this file with an appropriate text encoding
    with open(filename, encoding="latin_1") as fn :
        content = fn.readlines()

    #grab the line in optris files that matters
    for n in range(len(content)) :
        gpsline = content[n]
        if "$GPRMC" in gpsline :
            break

    try :
        gpsline = gpsline.replace(" ", "")
    except:
        return defaultReturn
    
    #Convert a char to an integer
    gpstrimmed = ""
    for c in gpsline :
        num = ord(c)
        if 9 < num < 100:
            gpstrimmed += c

    #grab relevant values in the parsed lines
    gpsarray = gpstrimmed.split(',')[3:7]

    #convert to an appropriate lat/long format
    try :
        latitude = float(gpsarray[0])/100
        longitude = float(gpsarray[2])/100
    except :
        return defaultReturn

    #give our lat/long the correct sign for South, West
    if gpsarray[1].lower() == 's' :
        latitude *= -1

    if gpsarray[3].lower() == 'w' :
        longitude *= -1

    return {"Filename":outputName, "Latitude":latitude, "Longitude":longitude, "Altitude":304.8}

#run Optris reader function
for filename in os.listdir(config["optrisData"]):
    if ".optris" in filename :
        print(filename)
        csv_list.append(read_optris(config["optrisData"] + "/" + filename))

#update date in filename as needed        
with open(config["optrisOutput"],"w", newline='') as csv_file:
    fieldnames = ['Filename', 'Latitude', 'Longitude', 'Altitude']
    csv_writer = csv.DictWriter(csv_file, delimiter = ",", fieldnames=fieldnames)
    csv_writer.writeheader()    
    csv_writer.writerows(csv_list)
        