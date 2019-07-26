import numpy as np
import sys
 
inname = sys.argv[1]
outname = sys.argv[2]
mn = int(sys.argv[3])
mx = int(sys.argv[4])

infile = open(inname)

#remove first line
with open(inname) as f :
	content = f.readlines()

dimensions = content[0]
dimensions = dimensions.split(",")
for n in range(len(dimensions)) :
	dimensions[n] = dimensions[n].strip('\n')

content = content[1:]
content = [x.strip() for x in content]
content = [x.strip('\n') for x in content]

#grab all content and store in 1d array of floats
arr = []
for n in content :
	for val in n.split(',') :
		arr.append(float(val))


#convert to numpy array, mask values in range
arr = np.array(list(map(float,arr)))
mask = (arr < mx) & (arr > mn)

outstr = ""
#outstr = dimensions[0] + "," + dimensions[1] + "\n"
print(outstr)

rowstr = ""
minRead = 1000
maxRead = 0
currentCol = 0
for n in range(len(arr)) :
	rowstr = rowstr + ("NaN," if not mask[n] else (str(arr[n]) + ","))

	currentCol += 1
	if currentCol >= int(dimensions[0]) :
		rowstr = rowstr[:-1] # strip comma and newline
		rowstr = rowstr + "\n"
		outstr = outstr + rowstr
		rowstr = ""
		currentCol = 0

	minRead = min(minRead, arr[n])
	maxRead = max(maxRead, arr[n])

print("Min value {0}, Max value {1}".format(minRead, maxRead))

outfile = open(outname, "w")
#outstr = str(outarray)[1:-1] #strip [] from the stringified array
#print(outstr)
outfile.write(outstr)
outfile.close()