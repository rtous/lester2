# lester2

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
pip install opencv-python==4.10.0.84
#pip install shapely==2.0.2
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
