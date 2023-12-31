import os
import numpy as np
from PIL import Image
from argparse import ArgumentParser
import cv2

import pgm_to_ppm


def display(ppm_images, fps) :
    delay_time = int(1000 / fps) # fps is in sec, delay_time is in ms
    
    for ppm_data in ppm_images :
        cv2.imshow("Output video from PPM images", ppm_data[..., ::-1])
        
        if cv2.waitKey(delay_time) & 0xFF == ord('q') :
            break
        

def save(ppm_images, output_path) :
    if args.ppm[-1] != "/" :
        args.ppm += "/"
        
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    index_frame = 0
    
    for ppm_data in ppm_images :
        img = Image.fromarray(ppm_data)
        img.save(output_path + "/" + str(index_frame) + ".ppm")
        
        index_frame += 1
    

args_parser = ArgumentParser(description="Application to visualize mpeg2dec flow")

args_parser.add_argument("--pgm", type=str, help="Input folder path containing PGM images", required=True)

args_parser.add_argument("--ppm", type=str, help="Output folder path to load PPM images, instead of showing them")

args_parser.add_argument("--bob_deinterlace", action="store_true", help="Deinterlace PPM images", default=False)

# From the mpeg2dec logs for the video bw_numbers.m2v, default fps is equal to 29.97.
args_parser.add_argument("--fps", type=float, help="Output video FPS when displayed", default=29.97)

args = args_parser.parse_args()

    
def main(args) :
    if args.pgm[-1] != "/" :
        args.pgm += "/"
    
    pgm_images = os.listdir(args.pgm)

    pgm_images = [filename for filename in pgm_images if filename.lower().endswith(".pgm")]
    
    pgm_images.sort(key=lambda s: int(''.join(filter(str.isdigit, s))))
    
    ppm_images = []
    
    print("Generating PPM RGB images ...")
    for pgm_path in pgm_images :
        ppm_images = ppm_images + pgm_to_ppm.generic_PGM_to_PPM(args.pgm + pgm_path, args.bob_deinterlace)

    if args.ppm == None :
        print("Displaying PPM RGB images in video ...")
        display(ppm_images, args.fps)
    
    else :
        print("Saving PPM RGB images into " + args.ppm + " ...")
        save(ppm_images, args.ppm)
        
    print("Finished !")
    
    return 0

main(args)