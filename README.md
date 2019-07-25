# Temperature CSV Parser

This python script is meant for parsing CSV files with a CSV file output.

## parse.py
Commandline arguments
>python parse.py \<flag\> \<input csv\> \<output csv\> \<min\> \<max\>

Flags
* -p : purge values in given range
* -r : replace values in given range with NaN   

## mask.py
This is just a different variant using numpy.

Commandline arguments
>python mask.py \<input csv\> \<output csv\> \<min\> \<max\>
