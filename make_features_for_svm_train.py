import numpy as np
import collections
import cv2
import pickle
def iou(mask1, mask2):
    mask1 = np.array(mask1, dtype=bool)
    mask2 = np.array(mask2, dtype=bool)
    mask1_area = np.count_nonzero( mask1 )
    mask2_area = np.count_nonzero( mask2 )
    intersection = np.count_nonzero( np.logical_and( mask1, mask2 ) )
    iou = intersection/(mask1_area+mask2_area-intersection)    
    return iou

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


import os



training = []
counter = 0

for i in os.listdir(os.getcwd() +'/my_groundtruth_hard/'):
        dmaot = []
        hqtrack = []
        glob_id = 0
        img = cv2.imread(os.getcwd()+'/groundtruth_train/'+i+'/color/00000001.jpg')
        height, width, channels = img.shape
        with open(os.getcwd()+'/my_groundtruth_hard/'+i) as f:
            gt=f.readlines()
        gt = [int(x) for x in gt]
        for j in os.listdir(os.getcwd() +'/dmaot_train/'+i):
            with open(os.getcwd() +'/dmaot_train/'+i+'/'+j) as f:
                    temp=f.readlines()
            temp = [x.split(',') for x in temp]
            dmaot.append(temp)
            with open(os.getcwd()+'/hqtrack_train/'+i+'/'+j) as f:
                    temp=f.readlines()
            temp = [x.split(',') for x in temp]
            hqtrack.append(temp)
        print(len(gt), len(dmaot[0]), len(hqtrack[0]))
        for h in range(len(gt)):
            #if gt[h] != -1:
                
            features_dmaot=[]
            features_hqtrack=[]
            dmaot_x = 0
            dmaot_y = 0
            hqtrack_x = 0
            hqtrack_y = 0
            dmaot_w = 0
            dmaot_h = 0
            hqtrack_w = 0
            hqtrack_h = 0
            okay = 0
            for p in range(len(dmaot)):
                dmaot_mask = np.zeros((height,width))
                print(i)
                print(gt[h], p,h)
                print(dmaot[p][h])
                
                dmaot_mask[int(dmaot[p][h][1]):int(dmaot[p][h][1])+int(dmaot[p][h][3]),int(dmaot[p][h][0][1:]):int(dmaot[p][h][0][1:])+int(dmaot[p][h][2])] = rle_to_mask([int(z) for z in dmaot[p][h][4:]],int(dmaot[p][h][2]),int(dmaot[p][h][3]))
                hqtrack_mask = rle_to_mask([int(z) for z in hqtrack[p][h][4:]],width,height)
                dmaot_rows = np.where(dmaot_mask==1)[0]
                dmaot_cols = np.where(dmaot_mask==1)[1]
                hqtrack_rows = np.where(hqtrack_mask==1)[0]
                hqtrack_cols = np.where(hqtrack_mask==1)[1]
                if len(dmaot_cols) != 0 and len(dmaot_rows) != 0 and len(hqtrack_rows) != 0 and len(hqtrack_cols) != 0:
                    dmaot_x += np.mean(dmaot_cols)
                    dmaot_y += np.mean(dmaot_rows)
                    hqtrack_x += np.mean(hqtrack_rows)
                    hqtrack_y += np.mean(hqtrack_cols)
                
                    dmaot_w += max(dmaot_cols)-min(dmaot_cols)+1
                    dmaot_h += max(dmaot_rows)-min(dmaot_rows)+1
                    hqtrack_w += max(hqtrack_cols)-min(hqtrack_cols)+1
                    hqtrack_h += max(hqtrack_rows)-min(hqtrack_rows)+1
                    okay += 1
            if okay > 0:
                
                features_dmaot = [dmaot_x/len(dmaot), dmaot_y/len(dmaot), dmaot_w/len(dmaot), dmaot_h/len(dmaot)]
                features_hqtrack = [hqtrack_x/len(dmaot), hqtrack_y/len(dmaot), hqtrack_w/len(dmaot), hqtrack_h/len(dmaot)]
                if gt[h] == -1: gt[h] = 1
                features = features_dmaot + features_hqtrack + [gt[h]]
                print(features)
                training.append(features)#, c])
print(counter)
print(sum([x[8] for x in training]),len(training))
with open("dmaothqtrack.pkl", "wb") as f: 
    training = pickle.dump(training, f)
