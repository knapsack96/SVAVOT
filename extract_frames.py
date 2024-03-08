
import cv2
import random

font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (100, 100)
  
# fontScale
fontScale = 4
  
# Line thickness of 2 px
thickness = 2
vidcap = cv2.VideoCapture("run.mp4")
# get total number of frames
totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
randomFrameNumber=random.randint(0, totalFrames)
# set frame position
vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
success, image = vidcap.read()
#cv2.putText(image, 'a', org, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
if success:
    cv2.imwrite("run1.jpg", image)
vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber+100)
success, image = vidcap.read()
#cv2.putText(image, 'b', org, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
if success:
    cv2.imwrite("run2.jpg", image)
vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber+200)
success, image = vidcap.read()
#cv2.putText(image, 'b', org, font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
if success:
    cv2.imwrite("run3.jpg", image)