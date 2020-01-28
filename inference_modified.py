''' Runs inference on a given GeoTIFF image.

This is a modified version of the file originally taken from:
https://github.com/isikdogan/deepwatermap

Meant to be replace the original file to enable the model to work with Sentinal2 Images

example:
$ python inference.py --checkpoint_path checkpoints/cp.135.ckpt \
    --image_path sample_data/sentinel2_example.tif --save_path water_map.png
'''

# Uncomment this to run inference on CPU if your GPU runs out of memory
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'



import argparse
import os

import deepwatermap
import tifffile as tiff
import numpy as np
import cv2
from PIL import Image
import Load_S2



def find_padding(v, divisor=32):
    v_divisible = max(divisor, int(divisor * np.ceil( v / divisor )))
    total_pad = v_divisible - v
    pad_1 = total_pad // 2
    pad_2 = total_pad - pad_1
    return pad_1, pad_2

def main(checkpoint_path, image_path, save_path, geotiff_save_path, geotiff_res):
    # load the model
    model = deepwatermap.model()
    model.load_weights(checkpoint_path)

    # Default resolution for created GeoTIFF Image is medium
    res = 1

    # load and preprocess the input image
    if os.path.isdir(image_path):
        image = Load_S2.load_S2(image_path, geotiff_save_path, res=res)
        # Check if a resolution is specified for the created GeoTIFF Image and set it
        if geotiff_res:
            if geotiff_res.lower() == 'low':
                res = 0
            elif geotiff_res.lower() == 'high':
                res = 2
    else:
        image = tiff.imread(image_path)
    pad_r = find_padding(image.shape[0])
    pad_c = find_padding(image.shape[1])
    image = np.pad(image, ((pad_r[0], pad_r[1]), (pad_c[0], pad_c[1]), (0, 0)), 'reflect')
    image = image.astype(np.float32)
    image = image - np.min(image)
    image = image / np.maximum(np.max(image), 1)

    # run inference
    image = np.expand_dims(image, axis=0)
    print('Model is predicting..')
    dwm = model.predict(image)
    print('Prediction made.')
    dwm = np.squeeze(dwm)
    dwm = dwm[pad_r[0]:-pad_r[1], pad_c[0]:-pad_c[1]]

    # soft threshold
    dwm = 1./(1+np.exp(-(16*(dwm-0.5))))
    dwm = np.clip(dwm, 0, 1)

    # save the output water map
    cv2.imwrite(save_path, dwm * 255)
    print('Image saved at', save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint_path', type=str,
                        help="Path to the dir where the checkpoints are stored")
    parser.add_argument('--image_path', type=str, help="Path to the input GeoTIFF image or Sentinal2 Directory")
    parser.add_argument('--save_path', type=str, help="Path where the output map will be saved")
    parser.add_argument('--geotiff_save_path', type=str, help="Path where the created GeoTIFF will be saved")
    parser.add_argument('--geotiff_res', type=str, help="Resolution of saved GeoTIFF image (Low | Medium | High)")
    args = parser.parse_args()
    main(args.checkpoint_path, args.image_path, args.save_path, args.geotiff_save_path, args.geotiff_res)
