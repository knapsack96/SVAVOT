#example
import pickle
import os
with open("svm1dmaothqtrack.pkl","rb") as f:
    res = pickle.load(f)
index = 0
for i in os.listdir(os.getcwd() +'/groundtruth_test/sequences/'):
    
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
       
           
        with open('dmaot_test/'+i+'/'+j) as d:
            dmaot = d.readlines()
       
        with open('dmaot_test/'+i+'/'+j+'_time.value') as qq:
            dmaot_time = qq.readlines()
        
        with open('hqtrack_test/'+i+'/'+j) as l:
            hqtrack = l.readlines()
        
        with open('hqtrack_test/'+i+'/'+j+'_time.value') as oo:
            hqtrack_time = oo.readlines()
        n = len(dmaot)
        with open("baseline/"+i+'/'+j+'.txt',"a") as f:
            with open("baseline/"+i+'/'+j+'_time.value',"a") as vv:
                for z in range(n):
                    if res[index+z] == 0: #hqtrack
                        f.write(hqtrack[z])
                        vv.write(hqtrack_time[z])
                    else: #dmaot
                        f.write(dmaot[z])
                        vv.write(dmaot_time[z])
        index += n
print(index, len(res))
