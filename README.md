# lester2

## Status

- Need to integrate the simplification code from lester-code
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

./subsample.sh $HOME/dev/lester2/data/scenes/test 0
python segment.py
python lowpoly_last.py data/scenes/test 1 5
