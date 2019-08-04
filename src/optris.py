
'''
Read optris files to extract gps coodinates.

This function expects the file's gps coordinates to be in a specific location within the file.
'''
def read_optris(filename) :
	with open(filename, encoding="latin_1") as fn :
		content = fn.readlines()

	gpsline = content[2]
	gpsline = gpsline.replace(" ", "")

	gpstrimmed = ""
	for c in gpsline :
		num = ord(c)
		if 9 < num < 100:
			gpstrimmed += c

	gpsarray = gpstrimmed.split(',')[3:7]

	latitude = float(gpsarray[0])/100
	longitude = float(gpsarray[2])/100

	if gpsarray[1].lower() == 's' :
		latitude *= -1

	if gpsarray[3].lower() == 'w' :
		longitude *= -1

	print("{0} contains coordinates | (lat:{1}, lng:{2})".format(filename, latitude, longitude))

	return (latitude, longitude)
