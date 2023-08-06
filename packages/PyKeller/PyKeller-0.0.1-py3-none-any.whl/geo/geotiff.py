#Geospatial TIFF Functions

import rasterio as rio
import numpy as np
import os

def subarctic_arctic_geotiff2height(lat,long):
   
    lat_range = []
    for j in np.arange(50,90,20):
        lat_range.append(j)
        
    long_range = []
    for i in np.arange(-180,210,30):
        long_range.append(i)
    
    if lat_range[0] <= lat < lat_range[1]:
        file_lat = str(lat_range[0])
    elif lat_range[1] < lat:
        file_lat = str(lat_range[1])
    
    for i in range(len(long_range)-1):
        if long_range[i] <= long < long_range[i+1]:
            file_long = str(abs(long_range[i]))
            if abs(long_range[i]) < 10:
                file_long = '0' + file_long
            if abs(long_range[i]) < 100:
                file_long = '0' + file_long
            if long_range[i] < 0:
                file_long += 'w'
            else:
                file_long += 'e'
    
    geo_file = 0
    files = os.listdir()
    for file in files:
        if file_long in file and file_lat in file:
            geo_file = file
    
    if geo_file == 0:
        return 0    
    
    geo_file = rio.open(geo_file)
    row,col = geo_file.index(long,lat)
    elev = geo_file.read()[0,:,:]
    ground_height = elev[row,col]
    
    if ground_height <= -32768:
        ground_height = 0
    
    return ground_height