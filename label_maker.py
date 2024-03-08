import numpy as np
import cv2
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


gt=[]
tctr=[]
outrack=[]
ou = 0
mo = 0

seq_ = []
for i in os.listdir(os.getcwd()+'/groundtruth_train/'):
    #img = cv2.imread(os.getcwd()+'/groundtruth_train/'+i+'/color/00000001.jpg')
    #height, width, channels = img.shape
    gt = []
    dmaot = []
    hqtrack = []
    seq_ = []
    if i[-3:] != 'txt':
        for j in os.listdir(os.getcwd()+'/groundtruth_train/'+i):
            if j[-3:] == 'txt': seq_.append(j)
        seq_ = sorted(seq_)
        for j in seq_:
            with open(os.getcwd()+'/groundtruth_train/'+i+'/'+j) as f:
                temp=f.readlines()
            temp = [x.split(',') for x in temp]
            gt.append(temp)
        #print(len(gt))
        for j in seq_:         
            with open(os.getcwd()+'/dmaot_train/'+i+'/'+j[:-4]) as f:
                temp=f.readlines()
            temp = [x.split(',') for x in temp]
            dmaot.append(temp)
        for j in seq_:
            with open(os.getcwd()+'/hqtrack_train/'+i+'/'+j[:-4]) as f:
                temp=f.readlines()
            temp = [x.split(',') for x in temp]
            hqtrack.append(temp)
        #for p in range(len(seq_)):
                       
        with open(os.getcwd()+'/my_groundtruth_hard/'+i,'a') as f:
            for h in range(len(gt[0])):
                what = '-1\n'
                iou_dmaot = 0
                iou_hqtrack = 0 
                okay = 0
                b = False
                for p in range(len(seq_)):
                    if gt[p][h][0][0] == 'm' and dmaot[p][h][0][0] == 'm' and hqtrack[p][h][0][0] == 'm':
                        
                        if dmaot[p][h] != ['m0', '0', '0', '0', '0\n'] and hqtrack[p][h] != ['m0', '0', '0', '0', '0\n']:
                            
                            #if gt[h][0][1] == '0':
                            gt_mask = rle_to_mask([int(z) for z in gt[p][h][4:]],int(gt[p][h][2]),int(gt[p][h][3]))
                            #print(gt_mask.shape)
                                
                            #if dmaot[h][0][1] == '0':
                            dmaot_mask = np.zeros((int(gt[p][h][3]),int(gt[p][h][2])))
                            dmaot_mask[int(dmaot[p][h][1]):int(dmaot[p][h][1])+int(dmaot[p][h][3]),int(dmaot[p][h][0][1:]):int(dmaot[p][h][0][1:])+int(dmaot[p][h][2])] = rle_to_mask([int(z) for z in dmaot[p][h][4:]],int(dmaot[p][h][2]),int(dmaot[p][h][3]))
                            #print(dmaot_mask.shape)
                            #hqtrack ha fatto una codifica strana, ha messo x,y,w,h propri e poi rle basandosi su x,y,w,h del groundtruth (0,0,1280,720).....
                            #if hqtrack[h][0][1] == '0':
                            hqtrack_mask = rle_to_mask([int(z) for z in hqtrack[p][h][4:]],int(gt[p][h][2]),int(gt[p][h][3]))
                            #print(hqtrack_mask.shape)
                            iou_dmaot += iou(gt_mask,dmaot_mask)
                            #print(iou_dmaot)
                            iou_hqtrack += iou(gt_mask,hqtrack_mask)
                            #print(iou_hqtrack)
                            okay += 1
                       
                if okay == len(seq_):
                   
                        
                    if iou_dmaot >= iou_hqtrack:
                        what = '1\n'
                    else:
                        what = '0\n'
                
                f.write(what)
                                           