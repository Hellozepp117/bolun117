
import random
files = [['cod-rna.txt',8,0.005]]
files=[ ['diabetes_scale.txt',8,0.3] ]

files=[ ['heart_scale.txt',13,1] ]

files=[ ['liver-disorders_scale.txt',5,1] ]

files=[ ['fourclass_scale.txt',2,1] ]


files=[ ['iris.scale.txt',4,1] ]

files=[ ['glass.scale.txt',9,1] ]

for file in files:
    d=file[1]
    f = open(file[0],'r')
    fptrain = open(file[0]+"_pTraing",'w')
    fptest = open(file[0]+"_pTest",'w')
    fmtrain = open(file[0]+"_mTraing",'w')
    fmtest = open(file[0]+"_mTest",'w')
    for line in f:
        data = line.split()
        y = int(data[0])
        if y<0:
            y=0
        xx=[0.0]*d    
        for feat in data[1:]:
            feat = feat.split(':')
            xx[int(feat[0])-1]=float(feat[1])
    


        feat = " ".join([str(x) for x in xx] )
        if random.random()<file[2]:
            fptrain.write(str(y)+":"+feat+"\n")
            fmtrain.write(str(y)+" "+feat+"\n")
        else:
            fptest.write(str(y)+":"+feat+"\n")
            fmtest.write(str(y)+" "+feat+"\n")
            
    
    f.close()
    fptrain.close()
    fptest.close()
    fmtrain.close()
    fmtest.close()



