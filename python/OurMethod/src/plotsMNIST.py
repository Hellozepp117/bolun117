import tensorflow as tf
import numpy as np
import math
import pickle 
from xml.sax.handler import feature_external_ges
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import matplotlib.pyplot as plt

from OutlierDetection import *

data  = pickle.load( open( "results/MNIST.txt_4.pickle", "rb" ) )



outliers = data['outliers']
 
od = OutlierDetection('MNIST.txt',True)


B = data['B']

# B = np.identity(od.d)

od.setBInSorter(B)

data=[]
f = open("MNIST_images.txt")
for line in f:
    data += [line]



print outliers

 

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
        filename="../../../icml2017/fig/MNIST_"+str(IDD)+"_"+str(od.labels[IDD])+"_"+str(j)+"_"+str(ID)+"_"+str(od.labels[ID])+".eps"
        f.savefig(filename)
        
    #plt.waitforbuttonpress()



