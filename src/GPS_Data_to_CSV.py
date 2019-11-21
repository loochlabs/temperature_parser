# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:22:49 2019

@author: kco77
"""

#%% Script for extracting GPS data from Optris files and writing to a CSV

import csv
import os

#enter file directory here where Optris files are saved
file_directory = "C:/Local/OneDrive - University of Canterbury/My Documents/PhD/Data Analysis/TIR/temperature_parser/data/Test_data_6_Nov/GPS_Files"

#create a list of the data for the CSV
csv_list = []

#run Optris reader function
for filename in os.listdir(file_directory):
    
    def read_optris(filename) :    
        #open this file with an appropriate text encoding
        with open(filename, encoding="latin_1") as fn :
            content = fn.readlines()
    
        #grab the line in optris files that matters
        gpsline = content[2]
        gpsline = gpsline.replace(" ", "")
        
    	#Convert a char to an integer
        gpstrimmed = ""
        for c in gpsline :
            num = ord(c)
            if 9 < num < 100:
                gpstrimmed += c
    
    	#grab relevant values in the parsed lines
        gpsarray = gpstrimmed.split(',')[3:7]
    
    	#convert to an appropriate lat/long format
        latitude = float(gpsarray[0])/100
        longitude = float(gpsarray[2])/100
    
    	#give our lat/long the correct sign for South, West
        if gpsarray[1].lower() == 's' :
            latitude *= -1
    
        if gpsarray[3].lower() == 'w' :
            longitude *= -1
    
        #these are the items that go in the list    
        csv_list = [filename + ".tif", latitude, longitude, "304.8"] 

#don't think we need these next few lines right now
#	print("{0} contains coordinates | (lat:{1}, lng:{2})".format(filename, latitude, longitude))
#
#	#return the lat/long as a tuple
#	return (latitude, longitude)
        
       

#update date in filename as needed        
with open("TIR_GPS_Data_6Nov.csv","w") as new_file:
    fieldnames = ["Filename", "Latitude", "Longitude", "Altitude"]
    csv_writer = csv.DictWriter(new_file,delimiter = ",",fieldnames=fieldnames)
    csv_writer.writeheader()
    rows = []
    
#    for row in csv_writer:
    csv_writer.writerow(csv_list)
        
#    new_file.close() #don't think I actually need this.
        