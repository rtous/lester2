#./stepX_compose_crowd.sh /Users/rtous/DockerVolume/flashback/output/scenes/tiktok2/sliderBW

#$1 = scene folder name
#$2 = 0 = color, 1 = Black and White

ANIMATION_DIR=$1

cd $ANIMATION_DIR

#2) GIF WITH NO BACKGROUND

ffmpeg -i renderImagesCrowd/image%04d.png -vf palettegen=reserve_transparent=1 palette.png

ffmpeg -framerate 30 -i renderImagesCrowd/image%04d.png -i palette.png -lavfi paletteuse=alpha_threshold=128 -gifflags -offsetting out_crowd.gif
