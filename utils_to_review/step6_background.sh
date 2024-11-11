#EXAMPLE: ./step6_background.sh $HOME/DockerVolume/flashback/data/scenes/imagesVideosNight3

#Assumes there's a $HOME/DockerVolume/flashback/data/imagesVideosMIB
# with a footage.mp4 file within.

WORKING_DIR=$1

cd $HOME/DockerVolume/flashback/6_background

source myvenv/bin/activate

python preprocessing.py -i $WORKING_DIR/imagesFull -o $WORKING_DIR

deactivate

cd $HOME/DockerVolume/CartoonGAN-Test-Pytorch-Torch

source myvenv/bin/activate

python test.py --input_dir $WORKING_DIR/backgrounds --output_dir $WORKING_DIR/backgroundsCartoonized --style Hosoda --gpu -1

deactivate

cd $HOME/DockerVolume/flashback