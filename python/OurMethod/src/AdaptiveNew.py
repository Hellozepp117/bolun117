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

 

odAll = OutlierDetection(filename , True)   
allFeatures = odAll.features
allLabels = odAll.labels
allN=len(allLabels)
print "All data:",allN , "d  = ",len(allFeatures[0])



Bident = np.identity(odAll.d)
odAll.setBInSorter(Bident)
Ri = []
# for i in selection:
for i in xrange(allN):
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
    Ri+=[ [i, outClassDistance / inClassDistance ] ] 

Ri.sort(key=lambda pair: pair[1])
zz = [ x[1] for x in Ri]
print "Missclassifications",sum([1 for x in zz if x < 1])    

plt.plot(zz)
plt.show()

 

labels=[]
features=[]
selection=[]
for x in Ri:
    i = x[0]
    if x[1]<200:
        features+=[allFeatures[i]]
        labels+=[allLabels[i]]
        selection+=[i]

print "totalPoints",len(labels)  

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

    
data  = pickle.load( open(   filename+"_"+str(5)+".pickle", "r" ) )     
# data  = pickle.load( open(   filename+"_INIT"+".pickle", "r" ) )     
     
    
    
B = data['B']

print B
    
odAll.setBInSorter(B)
Ri = []
# for i in selection:
for i in xrange(allN):
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
    print allLabels[i], allLabels[  inClassIDX], allLabels[outClassIDX], inClassDistance, outClassDistance, outClassDistance / inClassDistance

    Ri+=[ [i, outClassDistance / inClassDistance ] ] 
Ri.sort(key=lambda pair: pair[1])
yy = [ x[1] for x in Ri]
print "Missclassifications EUCLID",sum([1 for x in zz if x < 1])    
print "Missclassifications OUR",sum([1 for x in yy if x < 1])    


plt.plot(yy)
plt.plot(zz)

plt.show()
    


afddafasfa







asdfsadfafsafsa







 
print len(currentOultiers) , len(features)

skippPoints = {}
ALREADY_SELECTED={}
totalWorkingPoints=0
for x in selection:
    ALREADY_SELECTED[x]  = 1
    skippPoints[totalWorkingPoints]=x
    totalWorkingPoints=totalWorkingPoints+1


print "current ouliers:",len(currentOultiers)
print "working set:",len(labels)





for x in Ri:
    id = x[0]
    R = x[1]
    if R > 2:
        ALREADY_SELECTED.pop(id, 0)
        totalWorkingPoints=totalWorkingPoints-1
        li = selection.index(id)
        selection.pop(li)
        labels.pop(li)
        features.pop(li)
        
        
print "working set:",len(labels)
                
                
                

if True:
    od = OutlierDetection(None , True, labels, features)    
    epsilonMax, B = od.findLargestEpsilonRowAndColumnGeneration()
    print "Epsilon max = ", epsilonMax
    epsilon = epsilonMax*0.5
     
    t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B)
    currentOultiers = newOutliers
    print currentOultiers
    t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)
    for x in newOutliers:
        currentOultiers+=[x]
    print currentOultiers

data={}
data["B"]=od.B
data["outliers"]=currentOultiers  
data["epsilon"]=epsilon        
data['labels']=labels
data['features']=features
data['selection']=selection

pickle.dump( data, open( filename+"_S2"+".pickle", "wb" ) )  

