# LoadSentinal2Images
A module that prepares sentinal2 Satellite images to be used with DeepWaterMap deep learning algorithm by combining
the needed bands (B2,B3,B4,B8,B11,B12) and creating a GeoTIFF file

DeepWaterMap:
https://github.com/isikdogan/deepwatermap

installation:

    1- Follow these instructions to install rasterio and GDAL:
    https://rasterio.readthedocs.io/en/latest/installation.html
  
    2- Insert the Load_S2.py file into the DeepWaterMap directory
  
    3- Rename inferance_modified.py to inferance.py and replace the existing file in the DeepWaterMap directory
  
Usage:
  
  This module enables the user to pass a Sentinal2 Satellite image into DeepWaterMap 
  
Parametars:
    
    --image_path: In addition to passing a GeoTIFF file that the original algorithim enabled, an IMG_DATA directory
                  could be passed from Sentinal2 Satellite image folder
    --geotiff_save_path: The path and name of the GeoTIFF file created when combining the required S2 Bands Images
    
    --geotiff_res: The resloution of the output GeoTIFF image ( Low | Medium | High ). 
                   This peramater is not case sensitive with Medium as the default
                   
  
  
