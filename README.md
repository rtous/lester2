# lester2

## Status

- Anotation tool?
- Revert lester-code to its original state
- Check the git stater of seg4art
- segment.py still includes harcoded frames to avoid faces
- load colors from a file!!
- do a colab

## About

- This is a new version of https://github.com/rtous/lester-code, which in turn was an integration of:
  - https://github.com/rtous/Segment-and-Track-Anything
  - https://github.com/rtous/seg4art

- Also there's the old repo https://github.com/rtous/lester with results for the original paper.

## Introduction

- SAM2
- More accurate, better temporal consistency 

## Setup

```
git clone https://github.com/rtous/lester2.git
cd lester2

python3 -m venv myvenv
source myvenv/bin/activate

#Install SAM2 and download the checkpoints
cd sam2
pip install -e .
cd checkpoints
./download_ckpts.sh
cd ../..

#install other libraries
pip install matplotlib==3.9.2
pip install opencv-python==3.4.17.61
pip install shapely==2.0.2
pip install numpy==1.26.0
pip install imutils==0.5.4
pip install dlib==19.24.6
```
Download into models folder the model file of the dlib's HOG face detector (shape_predictor_68_face_landmarks.dat):
```
wget https://github.com/italojs/facial-landmarks-recognition/raw/refs/heads/master/shape_predictor_68_face_landmarks.dat -P models
```

### (just info) How SAM2 is included:

- Copied the sam2 subfolder from the sam2 repo to the root of the repo
- Copied setup.py and checkpoints from the sam2 repo to the root of the repo
- In segment.py changed:
```
  model_cfg = "sam2/configs/sam2.1/sam2.1_hiera_l.yaml"
```
by:
```
  model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
```

## Test

Subsample:

  ./subsample.sh $HOME/dev/lester2/data/scenes/test 0

Speficy the segmentation settings in a file (already done for the test scene):

  data/scenes/test/scene_segmentation_settings.py

And:

  python segment_latest.py data/scenes/test

Speficy the simplification settings in a file (already done for the test scene):

    data/scenes/test/scene_simplification_settings.py

And:

  python lowpoly_latest.py data/scenes/test 1 5

Generate final video:

  ./pngfinal2video.sh data/scenes/test 
  ./gifify.sh data/scenes/test

## Annotation tool

  python annotation_latest.py data/scenes/test

## Variations

### What happens if my video is not in the proper format?

```
ffmpeg -i data/scenes/SCENE/footage.mov -vcodec libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -r 24 -y -an data/scenes/SCENE/footage.mp4
```
### What happens if the video is very long but I don't want it all?

ffmpeg -ss 0.0 -i data/scenes/badcover/footage_long.mp4 -c:v libx264 -c:a aac -frames:v 4 data/scenes/badcover/footage.mp4

### What happens if the video is too long and I want to process it by parts?

Use:

slice_video.py

And then concat with:

A file concat.txt with:

file 'Video1_GE_res_part0.mp4'
file 'Video1_GE_res_part1.mp4'
file 'Video1_GE_res_part2.mp4'

And:

ffmpeg -f concat -i concat.txt -c copy Video1_GE_res.mp4


ffmpeg -f concat -i concat.txt -c copy Video1_GE_res.mp4



