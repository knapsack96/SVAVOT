import cv2
import os
from random import randrange
from PIL import Image, ImageDraw
import numpy as np
def rle_to_mask(rle, width, height):
    """ Converts RLE encoding to a binary mask. This is a Numba decorated function that is compiled just-in-time for faster execution.

    Args:
        rle (List[int]): RLE encoding of the mask
        width (int): Width of the mask
        height (int): Height of the mask

    Returns:
        np.ndarray: 2-D binary mask
    """

    # allocate list of zeros
    v = np.zeros(width * height, dtype=np.uint8)

    # set id of the last different element to the beginning of the vector
    idx_ = 0
    for i in range(len(rle)):
        if i % 2 != 0:
            # write as many 1s as RLE says (zeros are already in the vector)
            for j in range(rle[i]):
                v[idx_+j] = 1
        idx_ += rle[i]

    # reshape vector into 2-D mask
    # return np.reshape(np.array(v, dtype=np.uint8), (height, width)) # numba bug / not supporting np.reshape
    #return np.array(v, dtype=np.uint8).reshape((height, width))
    return v.reshape((height, width))
    
frames =[]
# for i in os.listdir('MOT20/test/MOT20-04/img1'):
#root = '/media/wprumm01/DISK_PhD_WP/Documents/Multi_object_tracking_CVPR/GNN_TrackPrediction/submit/img1/'
for i in os.listdir(r'C:\Users\vince\OneDrive\Desktop\VOTS2023\groundtruth_test\sequences\freesbiedog\color'):
# reading the input
#cap = cv2.VideoCapture("input.mp4")
  if i[-3:]=='jpg' :
    frames.append(i)
frames = sorted(frames)
print(frames[0])

img = cv2.imread('C:/Users/vince/OneDrive/Desktop/VOTS2023/groundtruth_test/sequences/freesbiedog/color/'+frames[0])

h,w,c = img.shape
output = cv2.VideoWriter(
        "freesbiedog.mp4", cv2.VideoWriter_fourcc(*'MPEG'), 
      30, (w, h))
masks = []
gt_masks = []
# with open(os.getcwd()+'/ReadyToVideo20/MOT20-04.txt') as f:
for i in os.listdir(r'C:\Users\vince\OneDrive\Desktop\VOTS2023\svavot\baseline\freesbiedog'):
    if i[-3:]=='bin': 
        with open('C:/Users/vince/OneDrive/Desktop/VOTS2023/svavot/baseline/freesbiedog/'+i) as f:
            masks.append(f.readlines())
        
            
color = [] 
for i in range(len(masks)):           
    color.append([randrange(256),randrange(256),randrange(256)])

for i in range(len(frames)):
    #img = cv2.imread(r'C:\Users\vince\OneDrive\Desktop\VOTS2023\groundtruth_test\sequences\dancingshoe\color\'+frames[i])
    image = cv2.imread('C:/Users/vince/OneDrive/Desktop/VOTS2023/groundtruth_test/sequences/freesbiedog/color/'+frames[i])
    #image.putalpha(128)
    for j in range(len(masks)):
        spl = masks[j][i].split(',')
        rle = [int(x) for x in spl[4:]]
        x = int(spl[0][1:]) 
        y = int(spl[1])
        w_ = int(spl[2])
        h_ = int(spl[3])
        mask = rle_to_mask(rle, w_, h_)
        #color_mask = np.ones_like(image)*255
        base_mask = np.zeros((image.shape[0],image.shape[1]))
        base_mask[y:y+h_,x:x+w_] = mask
        image[base_mask == 1] = [color[j][0], color[j][1], color[j][2]] # Choose any color you like
        #color_mask[base_mask == 0] = image[base_mask == 0]
        #masked_image = cv2.addWeighted(image, 0.8, color_mask, 0.2, 0)
        #image = masked_image
        #print(np.array(image).shape)
    #image.save('C:/Users/vince/OneDrive/Desktop/VOTS2023/prova/'+frames[i][:-3]+'png')
    output.write(image)
output.release()    



