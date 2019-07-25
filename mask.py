import numpy as np
import sys
 
inname = sys.argv[1]
outname = sys.argv[2]
mn = int(sys.argv[3])
mx = int(sys.argv[4])

infile = open(inname)
arr = list(map(int, infile.read().split(',')))
infile.close()
arr = np.array(arr)
mask = arr < mx

outarray = []
for n in range(len(arr)) :
	outarray.append("NaN" if not mask[n] else arr[n])

outfile = open(outname, "w")
outstr = str(outarray)[1:-1] #strip [] from the stringified array
outfile.write(str(outstr))
outfile.close()