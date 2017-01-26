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

data  = pickle.load( open(   filename+"_INIT"+".pickle", "r" ) ) 
# data  = pickle.load( open(   filename+"_S3"+".pickle", "r" ) ) 


B = data["B"] 
currentOultiers = data["outliers"]  
epsilon = data["epsilon"]        
labels = data['labels']
features = data['features']
selection = data['selection']

 
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



odAll.setBInSorter(B)
for k in currentOultiers:
    globalID = selection[k]
    i = globalID
# for globalID in xrange(allN):
#     i=globalID    
    currentLabel = allLabels[ globalID  ]
    
    closestPointID = -1
    minDistance = 1000
    #---------- want to find a closest points in DB to include them
    for j in xrange(allN):
        if j not in ALREADY_SELECTED and currentLabel == allLabels[j]:
            distance = odAll.sorter.computeDistanceBetweenTwoPoint(i, j)
            if distance < minDistance:
                minDistance = distance
                closestPointID = j
#     print "Outlier",i,"add ",closestPointID, minDistance
    labels+=[ allLabels[closestPointID] ]
    features+=[ allFeatures[closestPointID] ]
    selection+=[closestPointID]
    ALREADY_SELECTED[closestPointID]  = 1
    skippPoints[totalWorkingPoints]=closestPointID
    totalWorkingPoints=totalWorkingPoints+1


print "working set:",len(labels)


# remove points which are not needed (in the interiors)
# allN=100

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
    Ri+=[ [i, outClassDistance / inClassDistance ] ] 
Ri.sort(key=lambda pair: pair[1])
yy = [ x[1] for x in Ri]
print "Missclassifications",sum([1 for x in yy if x < 1])    


plt.plot(yy)
plt.plot(zz)

plt.show()
    


afddafasfa



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

