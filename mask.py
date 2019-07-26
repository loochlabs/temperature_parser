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

content = content[1:]
content = [x.strip() for x in content]
content = [x.strip('\n') for x in content]

arr = []
for n in content :
	for val in n.split(',') :
		arr.append(float(val))


#arr = list(map(int, content.split(',')))
#infile.close()
arr = np.array(list(map(float,arr)))
mask = (arr < mx) & (arr > mn)

outarray = []
minRead = 1000
maxRead = 0
for n in range(len(arr)) :
	outarray.append("NaN" if not mask[n] else arr[n])

	minRead = min(minRead, arr[n])
	maxRead = max(maxRead, arr[n])

print("Min value {0}, Max value {1}".format(minRead, maxRead))

outfile = open(outname, "w")
outstr = str(outarray)[1:-1] #strip [] from the stringified array
outfile.write(str(outstr))
outfile.close()