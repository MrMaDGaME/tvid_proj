import os
import numpy as np
from PIL import Image
from argparse import ArgumentParser
import cv2

import pgm_to_ppm


def display(ppm_images) :
    for ppm_data in ppm_images :
        cv2.imshow("Output video from PPM images", ppm_data[..., ::-1])
        
        if cv2.waitKey(25) & 0xFF == ord('q') :
            break
        

def save(ppm_images, output_path) :
    index_frame = 0
    
    for ppm_data in ppm_images :
        img = Image.fromarray(ppm_data)
        img.save(output_path + "/" + str(index_frame) + ".ppm")
        
        index_frame += 1
    

args_parser = ArgumentParser(description="Application to visualize mpeg2dec flow")

args_parser.add_argument("--pgm", type=str, help="Input folder path containing PGM images", required=True)

args_parser.add_argument("--ppm", type=str, help="Output folder path to load PPM images, instead of showing them")

args_parser.add_argument("--tff", action="store_true", help="Process images as TFF (top first field)", default=False)

args_parser.add_argument("--fps", type=int, help="Output video FPS when displayed", default=25)

args = args_parser.parse_args()

    
def main(args) :
    pgm_images = os.listdir(args.pgm)
    
    pgm_images.sort(key=lambda s: int(''.join(filter(str.isdigit, s))))
    
    ppm_images = []
    
    print("Generating PPM RGB images ...")
    for pgm_path in pgm_images :
        ppm_images = ppm_images + pgm_to_ppm.generic_PGM_to_PPM(args.pgm + pgm_path, args.tff)

    if args.ppm == None :
        print("Displaying PPM RGB images in video ...")
        display(ppm_images)
    
    else :
        print("Saving PPM RGB images into " + args.ppm + " ...")
        save(ppm_images, args.ppm)
        
    print("Finished !")
    
    return 0

main(args)