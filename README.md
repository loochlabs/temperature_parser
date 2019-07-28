# Temperature Processor

These python scripts are meant for parsing CSV files with a TIFF file output.

## cmd_convert
### Intermediate script for converting csv to tif

Commandline arguments
>python cmd_convert.py \<flag\> \<filename\> 

Flags
* -d : process all csv's in a directory
  * example
  * >python cmd_convert.py -d path/to/your/directory

* -f : process an individual file 
  * example
  * >python cmd_convert.py -f name_of_file.csv
