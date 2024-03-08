#example
import pickle
import os
with open("svm1dmaothqtrack.pkl","rb") as f:
    res = pickle.load(f)
index = 0
for i in os.listdir(os.getcwd() +'/groundtruth_test/sequences/'):
    os.makedirs(os.getcwd()+'/svavot/baseline/'+i)
    da_sort = []
    for j in os.listdir(os.getcwd() +'/dmaot_test/'+i):
        if j[-3:] == '001': da_sort.append(j)
    da_sort = sorted(da_sort)
    gt = []
    dmaot = []
    hqtrack = []
    dmaot_time = []
    hqtrack_time = []
    for j in da_sort:
        #if len(da_sort) == 1:
        #    varia = ''
        #else:
        #    varia = '_'+j.split('_')[-2]
        #with open(os.getcwd()+'/groundtruth_test/sequences/'+i+'/groundtruth'+varia+'.txt') as r:
        #    gt = r.readlines()
           
        with open('dmaot_test/'+i+'/'+j) as d:
            dmaot = d.readlines()
        #dmaot[0] = gt[0]
        with open('patch_swinb_de2_deaot_30_2_10_2023-09-16T07-35-43.210765/baseline/'+i+'/'+j+'_time.value') as qq:
            dmaot_time = qq.readlines()
        
        with open('hqtrack_test/'+i+'/'+j) as l:
            hqtrack = l.readlines()
        #hqtrack[0] = gt[0]
        with open('HQTrack_2023-06-18T14-14-13.570410/baseline/'+i+'/'+j+'_time.value') as oo:
            hqtrack_time = oo.readlines()
        n = len(dmaot)
        with open("svavot/baseline/"+i+'/'+j+'.bin',"a") as f:
            with open("svavot/baseline/"+i+'/'+j+'_time.value',"a") as vv:
                for z in range(n):
                    if res[index+z] == 0: #hqtrack
                        f.write(hqtrack[z])
                        vv.write(hqtrack_time[z])
                    else: #dmaot
                        f.write(dmaot[z])
                        vv.write(dmaot_time[z])
        index += n
print(index, len(res))