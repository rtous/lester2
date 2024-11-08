

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import torch
from sam2.build_sam import build_sam2
#from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 
import cv2

def RGB_to_opencv(c):
    return c[::-1]

#COLOR PALETTE (from segment.py from lester-code)
np.random.seed(200)
_palette = ((np.random.random((3*255))*0.7+0.3)*255).astype(np.uint8).tolist()
_palette = [0,0,0]+_palette
#c = _palette[id*3:id*3+3] USAGE

#Build our own dictionary for the colors
palette = {}
for i in range(255):
    palette[i] = _palette[i*3:i*3+3]


#load model
device = torch.device("cpu")
from sam2.build_sam import build_sam2_video_predictor
sam2_checkpoint = "sam2/checkpoints/sam2.1_hiera_large.pt"
#changed from the original:
#model_cfg = "sam2/configs/sam2.1/sam2.1_hiera_l.yaml"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
predictor = build_sam2_video_predictor(model_cfg, sam2_checkpoint, device=device)

#load frames
# `video_dir` a directory of JPEG frames with filenames like `<frame_index>.jpg`
video_dir = "/Users/rtous/dev/susan/Video1_GE/Video1_GE_part0"
# scan all the JPEG frame names in this directory
frame_names = [
    p for p in os.listdir(video_dir)
    if os.path.splitext(p)[-1] in [".jpg", ".jpeg", ".JPG", ".JPEG"]
]
frame_names.sort(key=lambda p: int(os.path.splitext(p)[0]))

#initialize inference state
inference_state = predictor.init_state(video_path=video_dir)

masks_points = []

#positive point mask0 (skin)
mask0_pos_x=750
mask0_pos_y=375

mask0_pos2_x=620
mask0_pos2_y=800

#mask0_pos3_x=780 #(glasses)
#mask0_pos3_y=300

mask0_pos3_x=620
mask0_pos3_y=800

#negative point mask0 
mask0_neg_x=750
mask0_neg_y=450

masks_points.append([np.array([[mask0_pos_x, mask0_pos_y],[mask0_pos2_x, mask0_pos2_y],[mask0_pos3_x, mask0_pos3_y],[mask0_neg_x, mask0_neg_y]], dtype=np.float32), np.array([1,1,1,0], np.int32)])

#positive point mask1 # (glasses)
mask1_pos_x=780
mask1_pos_y=300

masks_points.append([np.array([[mask1_pos_x, mask1_pos_y]], dtype=np.float32), np.array([1], np.int32)])

#positive point mask2 (shirt)
mask2_pos_x=720
mask2_pos_y=820

mask2_pos2_x=700
mask2_pos2_y=410

#negative point mask2 
mask2_neg_x=750
mask2_neg_y=450

masks_points.append([np.array([[mask2_pos_x, mask2_pos_y],[mask2_pos2_x, mask2_pos2_y],[mask2_neg_x, mask2_neg_y]], dtype=np.float32), np.array([1,1,0], np.int32)])

#positive point mask21 (shirt)
#mask21_pos_x=700
#mask21_pos_y=410

#mask21_pos2_x=700
#mask21_pos2_y=410

#masks_points.append([np.array([[mask21_pos_x, mask21_pos_y],[mask2_pos2_x, mask2_pos2_y]], dtype=np.float32), np.array([1,1], np.int32)])


#positive point mask3 (trousers)
mask3_pos_x=750
mask3_pos_y=900

masks_points.append([np.array([[mask3_pos_x, mask3_pos_y]], dtype=np.float32), np.array([1], np.int32)])

#positive point mask4 (jersey)
mask4_pos_x=750
mask4_pos_y=600

#negative point mask4 
mask4_neg_x=700
mask4_neg_y=410

masks_points.append([np.array([[mask4_pos_x, mask4_pos_y],[mask4_neg_x, mask4_neg_y]], dtype=np.float32), np.array([1,0], np.int32)])

#positive point mask5 (hair)
mask5_pos_x=700
mask5_pos_y=370

#negative point mask5 
mask5_neg_x=750
mask5_neg_y=375

masks_points.append([np.array([[mask5_pos_x, mask5_pos_y],[mask5_neg_x, mask5_neg_y]], dtype=np.float32), np.array([1,0], np.int32)])


ann_frame_idx = 0  # the frame index we interact with
ann_obj_id = 0  # give a unique id to each object we interact with (it can be any integers)

for mask_points in masks_points:
    print("add_new_points_or_box for ann_obj_id="+str(ann_obj_id))
    print(mask_points[0])
    points = mask_points[0]
    labels = mask_points[1]
    _, out_obj_ids, out_mask_logits = predictor.add_new_points_or_box(
        inference_state=inference_state,
        frame_idx=ann_frame_idx,
        obj_id=ann_obj_id,
        points=points,
        labels=labels,
    )
    
    # show the results on the current (interacted) frame
    print("showing one mask")
    mask = (out_mask_logits[ann_obj_id] > 0.0).cpu().numpy()
    color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask = mask.astype(np.uint8)
    mask_image =  mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(Image.open(os.path.join(video_dir, frame_names[ann_frame_idx])))
    for point in points:
        plt.plot(point[0], point[1], marker="o", markersize=10, markeredgecolor="green", markerfacecolor="green")
    #plt.plot(x2, y2, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
    #plt.plot(x3, y3, marker="o", markersize=10, markeredgecolor="green", markerfacecolor="green")
    plt.gca().imshow(mask_image)
    plt.show()
    

    ann_obj_id = ann_obj_id+1;



#Propagate the prompts to get the masklet across the video
# run propagation throughout the video and collect the results in a dict
video_segments = {}  # video_segments contains the per-frame segmentation results
for out_frame_idx, out_obj_ids, out_mask_logits in predictor.propagate_in_video(inference_state):
    video_segments[out_frame_idx] = {
        out_obj_id: (out_mask_logits[i] > 0.0).cpu().numpy()
        for i, out_obj_id in enumerate(out_obj_ids)
    }

scene = "test"
output_path = "data/scenes/"+scene+"/samtrack"
if not os.path.exists(output_path):
    os.makedirs(output_path)

#obtain dimensions of the image
first_frame = cv2.imread(os.path.join(video_dir, frame_names[0]))
height, width, channels = first_frame.shape

# show the results of the last frame
print("showing last mask")
for out_frame_idx in range(0, len(frame_names)):
    #create a white blank image (3 channels)
    blank_image_BGR = np.zeros((height,width,3), np.uint8)
    blank_image_BGR[:] = 255
    for out_obj_id, out_mask in video_segments[out_frame_idx].items():
        print("showing out_frame_idx="+str(out_frame_idx)+"/out_obj_id="+str(out_obj_id))
        mask = out_mask
        color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask = mask.astype(np.uint8)
        mask_image =  mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        '''
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(Image.open(os.path.join(video_dir, frame_names[ann_frame_idx])))
        #plt.plot(x, y, marker="o", markersize=10, markeredgecolor="green", markerfacecolor="green")
        #plt.plot(x2, y2, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")
        #plt.plot(x3, y3, marker="o", markersize=10, markeredgecolor="green", markerfacecolor="green")
        plt.gca().imshow(mask_image)
        plt.show()
        '''

        #mask is a vector of 0s and 1s. 
        #reshaping it as a matrix becomes a mask useful in opencv
        binary_mask = mask.reshape(h,w)
        
        #create a white blank image (3 channels)
        #blank_image_BGR = np.zeros((h,w,3), np.uint8)
        #blank_image_BGR[:] = 255

        #apply a color using the mask
        blank_image_BGR[binary_mask==1]=RGB_to_opencv(palette[(out_obj_id+10*1)%256])

    #save
    #cv2.imwrite(output_path+"/f"+str(out_frame_idx)+".png", blank_image_BGR)
    frame_filename_no_extension = os.path.splitext(frame_names[out_frame_idx])[0]
    cv2.imwrite(output_path+"/"+frame_filename_no_extension+'.png', blank_image_BGR)
