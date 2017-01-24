
import tensorflow as tf
import numpy as np
import math
import pickle 
from xml.sax.handler import feature_external_ges
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import matplotlib.pyplot as plt


f = open('CIFAR.txt','rU')
fw = open('CIFAR_f.txt','w')
i = 0
dic={}
problem=[]
for line in f:
    key, val = line.split(":")
    if val in dic:
        print i
        problem+=[i] 
    else:
        fw.write(line)
    dic[val] = 1
    
    i=i+1
f.close()
fw.close()    

data=[]
i = 0
f = open("CIFAR_images.txt")
fw = open("CIFAR_f_images.txt",'w')
for line in f:
    if i not in problem:
        fw.write(line) 
    data += [line]
    i=i+1
f.close()
fw.close()
#[7, 35, 64, 71, 73, 81]
for id in problem:
    print id
    
    pic = data[id]
    pic = np.array([float(x) for x in pic.split()])
    print pic
    
    pic2 = np.reshape(pic, (32,32,3), order='F')
    pic2 = pic.reshape(3,32,32).transpose(1,2,0)
         
    imgplot = plt.imshow(pic2)  
     
    plt.draw()   
    #fig.show()
    #
    plt.waitforbuttonpress()