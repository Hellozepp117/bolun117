import tensorflow as tf
import numpy as np
import math
import pickle 
from xml.sax.handler import feature_external_ges
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import matplotlib.pyplot as plt

from OutlierDetection import *

data  = pickle.load( open( "MNISTFULL.txt_FINAL.pickle", "rb" ) )



outliers = data['outliers']
 
od = OutlierDetection('MNISTFULL.txt',True)


B = data['B']

# B = np.identity(od.d)

# B = np.identity(od.d)

od.setBInSorter(B)

data=[]
f = open("MNISTFULL_images.txt")
for line in f:
    data += [line]



print outliers

print B 

N=10000
Ris = []
#for i in xrange((od.n)):
for i in xrange(N):   
    val = od.sorter.computeRi(i)
    Ris+= [val]

print Ris
print len(Ris)

# f = plt.figure()
# plt.show()
for selectedLabel in   [8,9]:

    Rv = []
    for i in xrange(N):
        if od.labels[i]==selectedLabel:
            Rv+=[ [i,Ris[i]]  ]
    
    Rv.sort(key=lambda pair: pair[1])
    
    print Rv
    zz = [ x[1] for x in Rv]
    
#     plt.plot(zz)
#     plt.title("$R_i$ class = "+str(selectedLabel))
#     plt.show()
    
    print "index ", selectedLabel, " number of outliers" ,   sum( [   1 for x in Rv if x[1] < 1  ]  )


    for indside in xrange( len(Rv)-10, len(Rv)  ):
        pair = Rv[indside]
        pic = data[pair[0]]
        pic = np.array([float(x) for x in pic.split()])
         
        pic2 = pic.reshape(28,28) 
             
    
        f = plt.figure()
        pic2 = pic.reshape(28,28) 
        imgplot = plt.imshow(pic2)   
        plt.draw()        
        filename="../../../icml2017/fig/MNISTFULL_inside_"+str(selectedLabel)+"_"+str(indside)+"_"+str(pair[0])+"_"+".eps"
        f.savefig(filename)
    
    left = -1
    right = -1
    for i in xrange(len(Rv)):
        if left==-1 and Rv[i][1]>1.0:
            left = i
        if right==-1 and Rv[i][1]>2:
            right = i
            break
            
        
    for boundary in xrange( left, min(left+10,right)  ):
        pair = Rv[boundary]
        pic = data[pair[0]]
        pic = np.array([float(x) for x in pic.split()])
         
        f = plt.figure()
        pic2 = pic.reshape(28,28) 
        imgplot = plt.imshow(pic2)   
        plt.draw()        
        filename="../../../icml2017/fig/MNISTFULL_boundary_"+str(selectedLabel)+"_"+str(boundary)+"_"+str(pair[0])+"_"+".eps"
        f.savefig(filename)
    if left > 10:
        left = 10

    for outli in xrange( 0, left  ):
        
        pair = Rv[outli]
        print "outlier ", pair[0], od.labels[pair[0]]
        pic = data[pair[0]]
        pic = np.array([float(x) for x in pic.split()])



        f = plt.figure()
        pic2 = pic.reshape(28,28) 
        imgplot = plt.imshow(pic2)   
        plt.draw()        
        filename="../../../icml2017/fig/MNISTFULL_outlier_"+str(selectedLabel)+"_"+str(outli)+"_"+str(pair[0])+"_"+".eps"
        f.savefig(filename)
          
        
        closestDistance = 10000
        closestId = -1
        for to in xrange(od.n):
            distance = od.sorter.computeDistanceBetweenTwoPoint(pair[0], to)
            if distance<closestDistance and to != pair[0]:
                closestId = to
                closestDistance = distance

        print "closest to outlier ", closestId, od.labels[closestId]

        
        pic = data[closestId]
        pic = np.array([float(x) for x in pic.split()])

        f = plt.figure()
        pic2 = pic.reshape(28,28) 
        imgplot = plt.imshow(pic2)   
        plt.draw()        
        filename="../../../icml2017/fig/MNISTFULL_outlier_"+str(selectedLabel)+"_"+str(outli)+"_"+str(pair[0])+"_closest_"+str(closestId)+"_"+str(od.labels[closestId])+".eps"
        f.savefig(filename)

              
#         imgplot = plt.imshow(pic2)   
#         plt.draw()
#          
#         plt.show()
#         










sadfasdfasfafa


for IDD in outliers[0:]:
# for IDD in []:    
    
    print "Picture",IDD,"Label",od.labels[IDD]
    so = []
    for to in xrange(od.n):
        distance = od.sorter.computeDistanceBetweenTwoPoint(IDD, to)
        so+=[ [distance,to] ] 
    so.sort(key=lambda pair: pair[0])
    
    for j in xrange(4):
        ID = so[j][1]
        print ID, "label",od.labels[ID]
        pic = data[ID]
        pic = np.array([float(x) for x in pic.split()])
         
        f = plt.figure()
        #pic2 = np.reshape(pic, (28,32,3), order='F')
        pic2 = pic.reshape(28,28) 
             
        imgplot = plt.imshow(pic2)   
        plt.draw()  
        #fig, ax = plt.subplots()
#         fig.savefig('MNIST'+str(ID)+'.eps', format='eps') 
#         plt.show()
#         filename="../../../icml2017/fig/MNIST_"+str(IDD)+"_"+str(od.labels[IDD])+"_"+str(j)+"_"+str(ID)+"_"+str(od.labels[ID])+".eps"
#         f.savefig(filename)
        
    #plt.waitforbuttonpress()



