import tensorflow as tf
import numpy as np
import math
import pickle 
from xml.sax.handler import feature_external_ges
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import matplotlib.pyplot as plt

print "test"


data=[]
f = open("dataset_cifar_images2.txt")
for line in f:
    data += [line]

#[7, 35, 64, 71, 73, 81]


pic = data[12]
pic = np.array([float(x) for x in pic.split()])
print pic

pic2 = np.reshape(pic, (32,32,3), order='F')
pic2 = pic.reshape(3,32,32).transpose(1,2,0)
     
imgplot = plt.imshow(pic2)  
 
plt.draw()   
#fig.show()
#
plt.waitforbuttonpress()



