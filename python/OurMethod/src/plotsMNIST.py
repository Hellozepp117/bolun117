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
f = open("dataset3_images.txt")
for line in f:
    data += [line]

ID = 121
pic = data[ID]
pic = np.array([float(x) for x in pic.split()])
print pic

#pic2 = np.reshape(pic, (28,32,3), order='F')
pic2 = pic.reshape(28,28) 
     
imgplot = plt.imshow(pic2)   
plt.draw()  
#fig, ax = plt.subplots()
#fig.savefig('MNIST'+str(ID)+'.eps', format='eps') 
plt.show()
#
plt.waitforbuttonpress()



