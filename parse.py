import sys

def purge(i, o, mn, mx):
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

def replace(i, o, mn, mx):
	infile = open(i)
	outfile = open(o, "w")
	arr = infile.read().split(',')
	outstr = ""
	for value in arr :
		if int(mn) < int(value) < int(mx) :
			outstr += value + ","
		else :
			outstr += "NaN,"

	outstr = outstr[:-1]
	outfile.write(outstr)

	infile.close()
	outfile.close()

if(len(sys.argv)) != 6 :
	raise Exception('invalid arguements')

flag = sys.argv[1]

infile = sys.argv[2]
outfile = sys.argv[3]
minRange = sys.argv[4]
maxRange = sys.argv[5]

log = "Parsing this fancy data between "
log += "[" + str(minRange) + "-" + str(maxRange) + "]"
print(log) 

if flag == "-p" :
	purge(infile, outfile, minRange, maxRange)
elif flag == "-r" :
	replace(infile, outfile, minRange, maxRange)
else :
	raise Exception('invalid flag arguement : {}'.format(flag))