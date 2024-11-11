import cv2

if __name__ == '__main__':
    vidPath = 'data/scenes/susan_GE1_all/footage.mp4'
    #shotsPath = 'data/scenes/susan_GE1_all/%d.avi' # output path (must be avi, otherwize choose other codecs)
    shotsPath = 'data/scenes/susan_GE1_all/%d.mp4' # output path (must be avi, otherwize choose other codecs)
    segRange = [(0,99),(100,199),(200,299)] # a list of starting/ending frame indices pairs

    cap = cv2.VideoCapture(vidPath)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #fourcc = int(cv2.VideoWriter_fourcc('X','V','I','D')) # XVID codecs
    fourcc = cv2.VideoWriter_fourcc(*'X264')

    for idx,(begFidx,endFidx) in enumerate(segRange):
        writer = cv2.VideoWriter(shotsPath%idx,fourcc,fps,size)
        cap.set(cv2.CAP_PROP_POS_FRAMES,begFidx)
        ret = True # has frame returned
        while(cap.isOpened() and ret and writer.isOpened()):
            ret, frame = cap.read()
            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
            if frame_number < endFidx:
                writer.write(frame)
            else:
                break
        writer.release()