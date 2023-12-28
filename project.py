import os
import numpy as np
from PIL import Image
from argparse import ArgumentParser
#import cv2

import pgm_to_ppm

    
def display(ppm_images) :
    for ppm_data in ppm_images :
        img = Image.fromarray(ppm_images[0])
        img.show()
        

def save(ppm_images, output_path) :
    index_frame = 0
    for ppm_data in ppm_images :
        img = Image.fromarray(ppm_data)
        img.save(output_path + "/" + str(index_frame) + ".ppm")
        index_frame += 1
    

args_parser = ArgumentParser(description="Application to visualize mpeg2dec flow")

args_parser.add_argument("--pgm", type=str, help="Folder input path containing PGM images", required=True)

args_parser.add_argument("--ppm", type=str, help="Folder output path to load PPM images, instead of showing them")

args_parser.add_argument("--tff", action="store_true", help="Process images as top first field", default=False)

args = args_parser.parse_args()
    
    
def main(args) :
    pgm_images = os.listdir(args.pgm)
    
    pgm_images.sort(key=lambda s: int(''.join(filter(str.isdigit, s))))
    
    print(pgm_images)
    print(args.pgm)
    
    ppm_images = []
    
    for pgm_path in pgm_images :
        ppm_images = ppm_images + pgm_to_ppm.generic_PGM_to_PPM(args.pgm + pgm_path, args.tff)

    if args.ppm == None :
        display(ppm_images)
    
    else :
        save(ppm_images, args.ppm)
    
    return 0

main(args)