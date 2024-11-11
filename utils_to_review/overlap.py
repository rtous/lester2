import cv2
from os import listdir
from os.path import isfile, join, splitext 
import numpy as np
import random
import pathlib
import sys


#from: https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background


REFERENCEPATH = "output/scenes/tiktok2/sliderBW/renderImages"
TARGETPATH = "output/scenes/tiktok2/sliderBW/renderImagesCrowd"

pathlib.Path(TARGETPATH).mkdir(parents=True, exist_ok=True)

imageFiles = [f for f in listdir(REFERENCEPATH) if isfile(join(REFERENCEPATH, f))]

img0  = cv2.imread(REFERENCEPATH+"/"+imageFiles[0], cv2.IMREAD_UNCHANGED)

num_rows, num_cols = img0.shape[:2]

blank_image = np.zeros((num_rows,num_cols,3), np.uint8)

#translation_matrix = np.float32([ [1,0,70], [0,1,110] ])


for filename in imageFiles:
    img  = cv2.imread(REFERENCEPATH+"/"+filename, cv2.IMREAD_UNCHANGED)
    if (img is None):
            sys.exit("Error reading "+REFERENCEPATH+"/"+filename)
    imgCrowd = np.zeros((num_rows,num_cols,3), np.uint8)
    imgCrowd[:,:] = (255,255,255)
    #imgCrowd = np.zeros((num_rows,num_cols,4), np.uint8)
    for person_number in range(0, 10):
        #pos = random.randint(0,num_rows/2)
        overlay_transparent(imgCrowd, img, person_number*50, 0)
        cv2.imwrite(TARGETPATH+"/"+filename, imgCrowd)
    cv2.imwrite(TARGETPATH+"/"+filename, imgCrowd)

#cv2.namedWindow('Translation', cv2.WINDOW_NORMAL)
#cv2.imshow('Translation', blank_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
	


	