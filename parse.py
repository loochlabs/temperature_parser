import sys

def parse(i, o, mn, mx):
	infile = open(i)
	outfile = open(o, "w")
	arr = infile.read().split(',')
	outstr = ""
	for value in arr :
		if int(mn) < int(value) < int(mx) :
			outstr+= value + ","

	outstr = outstr[:-1]
	outfile.write(outstr)

	infile.close()
	outfile.close()

infile = sys.argv[1]
outfile = sys.argv[2]
minRange = sys.argv[3]
maxRange = sys.argv[4]

log = "Parsing this fancy data between "
log += "[" + str(minRange) + "-" + str(maxRange) + "]"
print(log) 

parse(infile, outfile, minRange, maxRange)