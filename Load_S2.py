import rasterio
from os import listdir
from os.path import isfile, join
import tifffile as tiff


def load_S2(img_data_path, output_path, res=2):
    """
        Creates a GeoTIFF file ready to be inputted on the DeepWaterMap model

        img_data_path: The path to the IMG_DATA file in sentinal2 file

        output_path: The path where the combined bands GeoTIFF image will be saved

        res: Higher resolution results in a bigger file size
            0: Low
            1: Medium
            2: High


        Returns an instance of the image
    """

    # Create a list of the required band images B2,B3,B4,B8,B11,B12
    onlyfiles = [f for f in listdir(img_data_path) if isfile(join(img_data_path, f))]
    band_paths = []
    for file in onlyfiles:
        band_name = file.split('_')[2].split('.')[0]
        if band_name == 'B02' or band_name == 'B03' or band_name == 'B04' or band_name == 'B08' or band_name == 'B11' or band_name == 'B12':
            extension = file.split('.')
            extension = extension[len(extension) - 1]
            if extension == 'jp2':
                band_paths.append(img_data_path + '/' + file)

    # Load the band images into memory
    band2 = rasterio.open(band_paths[0], driver='JP2OpenJPEG')  # blue
    band3 = rasterio.open(band_paths[1], driver='JP2OpenJPEG')  # green
    band4 = rasterio.open(band_paths[2], driver='JP2OpenJPEG')  # red
    band8 = rasterio.open(band_paths[3], driver='JP2OpenJPEG')  # NIR
    band11 = rasterio.open(band_paths[4], driver='JP2OpenJPEG')  # SWIR1
    band12 = rasterio.open(band_paths[5], driver='JP2OpenJPEG')  # SWIR2

    # Determine the resolution of the GeoTIFF image based on the input
    width = 0
    height = 0
    if res == 0:
        width = band11.width
        height = band11.height
    elif res == 1:
        width = (band2.width + band11.width) / 2
        height = (band2.height + band11.height) / 2
    elif res == 2:
        width = band2.width
        height = band2.height

    # Create the GeoTIFF Image
    output = rasterio.open(output_path, 'w', driver='Gtiff',
                           width=width, height=height,
                           count=6,
                           crs=band2.crs,
                           transform=band2.transform,
                           dtype=band2.dtypes[0]
                           )

    output.write(band2.read(1), 1)  # blue
    output.write(band3.read(1), 2)  # green
    output.write(band4.read(1), 3)  # red
    output.write(band8.read(1), 4)  # NIR
    output.write(band11.read(1), 5)  # SWIR1
    output.write(band12.read(1), 6)  # SWIR2

    size = output.size()
    # Free the file from memory
    output.close()

    print('GeoTiff file created')

    # Read an instance of the image and return it
    image = tiff.imread(output_path)
    return image
