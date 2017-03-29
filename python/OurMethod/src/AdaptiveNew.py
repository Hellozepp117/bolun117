from __future__ import division

from OutlierDetection import *
import random
import pickle 



import matplotlib.pyplot as plt



# filename = 'MNIST.txt'
filename = 'MNISTFULL.txt'
# filename = 'dataset_cifar2.txt'
# filename = 'dataset_cifar_sub.txt'
# filename = 'dataset_cifar2_sub.txt'
# filename = 'CIFAR.txt'


# filename = 'synthetic.txt'

# filename = 'CIFAR5.txt'

filename = 'datasets/cod-rna.txt_pTraing' 
filenameMatlab = 'datasets/cod-rna.txt_mTraing' 
filenameData = 'datasets/cod-rna.txt_pTestsh' 


filename = 'datasets/diabetes_scale.txt_pTraing' 
filenameMatlab = 'datasets/diabetes_scale.txt_mTraing' 
filenameData = 'datasets/diabetes_scale.txt_pALL' 

filename ='datasets/iris.scale.txt_pTraing'
filenameData = 'datasets/iris.scale.txt_pTraing'
filenameMatlab = 'datasets/iris.scale.txt_mTraing' 



odAll = OutlierDetection(filenameData , True)   
allFeatures = odAll.features
allLabels = odAll.labels
allN=len(allLabels)
print "All data:",allN , "d  = ",len(allFeatures[0])



Bident = np.identity(odAll.d)
odAll.setBInSorter(Bident)
Ri = []
# for i in selection:
for i in xrange(allN):
    if i%1000==0:
        print i ,"/",allN
    inClassDistance = 10000
    outClassDistance = 10000
    inClassIDX=-1
    outClassIDX = -1
    for j in xrange(allN):#selection:
        if i != j:
            distance = odAll.sorter.computeDistanceBetweenTwoPoint(i, j)
            if allLabels[i]==allLabels[j] and distance< inClassDistance:
                inClassDistance = distance
                inClassIDX = j
            if allLabels[i]!=allLabels[j] and distance< outClassDistance:
                outClassDistance = distance
                outClassIDX = j
    if inClassDistance==0:
        Ri+=[ [i, 2 ] ] 
    else:                        
        Ri+=[ [i, outClassDistance / (0.0000 +inClassDistance) ] ] 


Ri.sort(key=lambda pair: pair[1])
zz = [ x[1] for x in Ri]
print "Missclassifications",sum([1 for x in zz if x < 1])    




# plt.plot(zz)
# plt.show()

 

# labels=[]
# features=[]
# selection=[]
# for x in Ri:
#     i = x[0]
#     if x[1]<200:
#         features+=[allFeatures[i]]
#         labels+=[allLabels[i]]
#         selection+=[i]
# print "totalPoints",len(labels)  

# for it in xrange(1):
# 
#     od = OutlierDetection(None , True, labels, features)    
#     epsilonMax, B = od.findLargestEpsilonRowAndColumnGeneration()
#     print "Epsilon max = ", epsilonMax
#     epsilon = epsilonMax*0.000001
#     
#     t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B)
#     currentOultiers = newOutliers
#     print currentOultiers
#     t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)
#     for x in newOutliers:
#         currentOultiers+=[x]
#     print currentOultiers
# 
#     B = od.B
#     
# data={}
# data["B"]=B
# data["outliers"]=currentOultiers  
# data["epsilon"]=epsilon        
# data['labels']=labels
# data['features']=features
# data['selection']=selection
# 
# pickle.dump( data, open( filename+"_NEW_0"+".pickle", "wb" ) )  

    
# data  = pickle.load( open(   filename+"_"+str(1)+".pickle", "r" ) )     
# data  = pickle.load( open(   filename+"_INIT"+".pickle", "r" ) )     
data  = pickle.load( open(   filename+"_FINAL"+".pickle", "r" ) )     
B = data['B']
odAll.setBInSorter(B)


odAll.sorter.resetOutliers()
 
Ri = []
# for i in selection:
for i in xrange(allN):
    inClassDistance = 10000
    outClassDistance = 10000
    inClassIDX=-1
    outClassIDX = -1
    for j in xrange(allN):#selection:
        if i != j  :
            distance = odAll.sorter.computeDistanceBetweenTwoPoint(i, j)
            if allLabels[i]==allLabels[j] and distance< inClassDistance:
                inClassDistance = distance
                inClassIDX = j
            if allLabels[i]!=allLabels[j] and distance< outClassDistance:
                outClassDistance = distance
                outClassIDX = j
#     print allLabels[i], allLabels[  inClassIDX], allLabels[outClassIDX], inClassDistance, outClassDistance, outClassDistance / inClassDistance
    if inClassDistance==0:
        Ri+=[ [i, 2 ] ] 
    else:                        
        Ri+=[ [i, outClassDistance / (0.0000 +inClassDistance) ] ] 

Ri.sort(key=lambda pair: pair[1])
yy = [ x[1] for x in Ri]
print "Missclassifications EUCLID",sum([1 for x in zz if x < 1])    
print "Missclassifications OUR",sum([1 for x in yy if x < 1])    


outliers={}
print "search for outliers!!!"
for x in Ri:
    sample = x[0]
    val = x[1]
    if val<1:
        cRi = odAll.sorter.computeRi(sample)
        if cRi<1:
            outliers[sample]=1
            odAll.sorter.setOutlier(sample)


Ri = []
# for i in selection:
for i in xrange(allN):
    inClassDistance = 10000
    outClassDistance = 10000
    inClassIDX=-1
    outClassIDX = -1
    for j in xrange(allN):#selection:
        if i != j and j not in  outliers:
            distance = odAll.sorter.computeDistanceBetweenTwoPoint(i, j)
            if allLabels[i]==allLabels[j] and distance< inClassDistance:
                inClassDistance = distance
                inClassIDX = j
            if allLabels[i]!=allLabels[j] and distance< outClassDistance:
                outClassDistance = distance
                outClassIDX = j
#     print allLabels[i], allLabels[  inClassIDX], allLabels[outClassIDX], inClassDistance, outClassDistance, outClassDistance / inClassDistance
    if inClassDistance==0:
        Ri+=[ [i, 2 ] ] 
    else:                        
        Ri+=[ [i, outClassDistance / (0.0000 +inClassDistance) ] ] 

Ri.sort(key=lambda pair: pair[1])
yy = [ x[1] for x in Ri]
print "Missclassifications EUCLID",sum([1 for x in zz if x < 1])    
print "Missclassifications OUR",sum([1 for x in yy if x < 1])    




for K in [1,3,5,7,11]:
    f = open(filenameMatlab+str('_matlab_'+str(K)),'rU')
    
    M = [ [ float(x) for x in line.split() ] for line in f]
     
    B = np.array(M)
     
    
    odAll.setBInSorter(B)
    Ri = []
    # for i in selection:
    for i in xrange(allN):
        if i%1000==0:
            print i ,"/",allN
        inClassDistance = 10000
        outClassDistance = 10000
        inClassIDX=-1
        outClassIDX = -1
        for j in xrange(allN):#selection:
            if i != j:
                distance = odAll.sorter.computeDistanceBetweenTwoPoint(i, j)
                if allLabels[i]==allLabels[j] and distance< inClassDistance:
                    inClassDistance = distance
                    inClassIDX = j
                if allLabels[i]!=allLabels[j] and distance< outClassDistance:
                    outClassDistance = distance
                    outClassIDX = j
#         print allLabels[i], allLabels[  inClassIDX], allLabels[outClassIDX], inClassDistance, outClassDistance, outClassDistance / inClassDistance
        if inClassDistance==0:
            Ri+=[ [i, 2 ] ] 
        else:                        
            Ri+=[ [i, outClassDistance / (0.0000 +inClassDistance) ] ] 

    
    Ri.sort(key=lambda pair: pair[1])
    zz = [ x[1] for x in Ri]
    print K,"Missclassifications",sum([1 for x in zz if x < 1])    







# 
# plt.plot(yy)
# plt.plot(zz)
#  
# plt.show()

 