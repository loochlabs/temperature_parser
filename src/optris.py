
'''
Read optris files to extract gps coodinates.

This function expects the file's gps coordinates to be in a specific location within the file.
'''
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

	print("{0} contains coordinates | (lat:{1}, lng:{2})".format(filename, latitude, longitude))

	#return the lat/long as a tuple
	return (latitude, longitude)
