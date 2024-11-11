import sys
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

def main(scene_path):
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
    video_dir = scene_path+"/imagesFull"
    # scan all the JPEG frame names in this directory
    frame_names = [
        p for p in os.listdir(video_dir)
        if os.path.splitext(p)[-1] in [".jpg", ".jpeg", ".JPG", ".JPEG"]
    ]
    frame_names.sort(key=lambda p: int(os.path.splitext(p)[0]))

    #initialize inference state
    inference_state = predictor.init_state(video_path=video_dir)

    '''
    #This takes the specific scene segmentation settings from the file data/scenes/test/scene_segmentation_settings.py
    import sys
    sys.path.append("data/scenes/test/")
    from scene_segmentation_settings import *
    '''

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

if __name__ == "__main__":
    print("Ruben's SAM-Track launcher")
    scene_path = sys.argv[1]
    print("scene_path:", scene_path)

    #This takes the specific scene segmentation settings from the file data/scenes/test/scene_segmentation_settings.py
    sys.path.append(scene_path+"/")
    from scene_segmentation_settings import *

    main(scene_path)