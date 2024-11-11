import cv2

if __name__ == '__main__':
    vidPath = 'data/scenes/susan_GE1_all/footage.mp4'
    #shotsPath = 'data/scenes/susan_GE1_all/%d.avi' # output path (must be avi, otherwize choose other codecs)
    shotsPath = 'data/scenes/susan_GE1_all/footage_part%d.mp4' # output path (must be avi, otherwize choose other codecs)
    #segRange = [(0,99),(100,199),(200,299),(300,399)] # a list of starting/ending frame indices pairs

    cap = cv2.VideoCapture(vidPath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    segRange=[]
    i = 0
    start_frame = 0
    while start_frame<length :
        if start_frame+100 < length:
            segRange.append((start_frame, start_frame+100-1))
        else:
            segRange.append((start_frame, length-1))
        i = i+1
        start_frame = start_frame+100

    print(segRange)


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
