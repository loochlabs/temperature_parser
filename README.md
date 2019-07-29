# Temperature Processor
![alt text](https://github.com/thecalooch/temperature_parser/blob/master/images/heatmap_example.png)

These python scripts are meant for parsing CSV files into an image heatmap.

## Temperature Color Range
![alt text](https://github.com/thecalooch/temperature_parser/blob/master/images/temperature_range.png)

## Getting Started
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
