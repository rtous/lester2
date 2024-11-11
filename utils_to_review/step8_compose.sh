#./step8_compose.sh /Users/rtous/DockerVolume/flashback/output/scenes/topgun_scene1/shae /Users/rtous/DockerVolume/flashback/output/scenes/topgun_scene1 0 0 640 480

#$1 = scene folder name
#$2 = 0 = color, 1 = Black and White

ANIMATION_DIR=$1
BACKGROUND_DIR=$2
BW=$3
FIXED_BACKGROUND=$4
OUTPUTWIDTH=$5
OUTPUTHEIGHT=$6

cd $ANIMATION_DIR

#1) VIDEO WITH FIXED OR CHANGING BACKGROUND

#scale backgroundsCartoonized
mkdir -p backgroundsCartoonizedScaled

mkdir -p renderImagesScaled

ffmpeg -i $BACKGROUND_DIR/backgroundsCartoonized/%03d_background_Hosoda.jpg -vf scale=$OUTPUTWIDTH:$OUTPUTHEIGHT backgroundsCartoonizedScaled/%03d_background_Hosoda.jpg

#scale renderImages
ffmpeg -i renderImages/image%04d.png -vf scale=$OUTPUTWIDTH:$OUTPUTHEIGHT renderImagesScaled/image%04d.png

#combine renderImages and backgroundsCartoonized
mkdir -p renderImagesCombined

if [ $FIXED_BACKGROUND -eq 0 ]
then
	ffmpeg -y -i backgroundsCartoonizedScaled/%03d_background_Hosoda.jpg -i renderImagesScaled/image%04d.png -filter_complex overlay=0:0 renderImagesCombined/%03d.jpg
else
	ffmpeg -y -i backgroundsCartoonizedScaled/001_background_Hosoda.jpg -i renderImagesScaled/image%04d.png -filter_complex overlay=0:0 renderImagesCombined/%03d.jpg
fi

#put the images together to make the MP4 video
ffmpeg -y -r 25 -i renderImagesCombined/%03d.jpg -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4

#2) GIF WITH NO BACKGROUND

ffmpeg -i renderImages/image%04d.png -vf palettegen=reserve_transparent=1 palette.png

ffmpeg -framerate 30 -i renderImages/image%04d.png -i palette.png -lavfi paletteuse=alpha_threshold=128 -gifflags -offsetting out.gif

#About changing start frame:

#-loop 1
#-start_number 0

