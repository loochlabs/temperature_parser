# Temperature Processor
A Python library for converting Optris temperature readings into undistorted/flattened images. 

## Dependencies
* numpy
* opencv

# Workflow for TIR Image Processing

1. Create mask for removing temperature array edges. 

2. Convert temperature CSVs to tiffs  
   * Find min and max temperatures across all temp arrays.  
   * Convert the temp range (based on the above min and max temps) to RGB colors.  
   * Create RGB array.  
   * Populate array with RGB values.  
   * Apply image mask to remove edges.  
   * Make sure orientation is landscape and image is right side up.  
   * Create .tif file for each CSV.  
   
3. Fisheye lens calibration  
   * Convert calibration CSV files to tifs.  
   * Convert to black and white.  
   * Run opencv module to find parameters needed for distortion correction.   
   * Carry out distortion correction on tifs.  
   * Save final tifs to a folder.  
   
4. GPS data parser  
   * Read all Optris files in a directory.  
   * From each file get filename and add '.tif' to filename.  
   * Get latitude and longitude. (e.g. -43.3935689, 172.2936697).  
   * Add altitude of 304.8 to each latitude and longitude.  
   * Create one output CSV with GPS coordinates for all tifs.   
   
5. Create image mosaic in Metashape    
   * Load tifs.  
   * Load CSV with GPS data.  
   * Stitch images.  
   * Note: will likely need to process images in batches.  
   * Desired outputs: jpg, kml files. Shapefile compatible with Arcmap if possible.  
   
# Getting Started
## Intermediate script for converting csv to tif

Commandline arguments
>python cmd_convert.py \<flag\> \<filename\> 

Flags
* -d : process all csv's in a directory
  * example
  * >python cmd_convert.py -d path/to/your/directory

* -f : process an individual file 
  * example
  * >python cmd_convert.py -f name_of_file.csv
  
## Expected Distorted Output
![alt text](https://github.com/thecalooch/temperature_parser/blob/master/images/heatmap_example.png)

## Temperature Color Range
![alt text](https://github.com/thecalooch/temperature_parser/blob/master/images/temperature_range.png)



