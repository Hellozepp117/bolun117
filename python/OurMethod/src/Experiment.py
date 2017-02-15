from __future__ import division

from OutlierDetection import *

import pickle 







# filename = 'MNIST.txt'
filename = 'CIFAR_f.txt'
# filename = 'dataset_cifar2.txt'
# filename = 'dataset_cifar_sub.txt'
# filename = 'dataset_cifar2_sub.txt'
# filename = 'CIFAR.txt'
filename = 'MNISTFULL.txt'

filename = 'datasets/cod-rna.txt_pTraing'
filename = 'datasets/diabetes_scale.txt_pTraing'


filename = "syntheticNoOutliers.txt"


filename = 'datasets/diabetes_scale.txt_pALL'


#filename = 'datasets/heart_scale.txt_pTraing'

#filename = 'datasets/liver-disorders_scale.txt_pTraing'


filename = 'datasets/fourclass_scale.txt_pTraing'

filename = 'datasets/iris.scale.txt_pTraing'

 

filename='syntheticWithOutliers.txt'


# filename = 'synthetic.txt'

od = OutlierDetection(filename , True)    



# filename = '50_c2_d2.txt'
# od = OutlierDetection(filename , False)    
 


if True:
    epsilonMax, B = od.findLargestEpsilonRowAndColumnGeneration()
    
    
    
    print "Epsilon max = ", epsilonMax
    epsilon = epsilonMax *0.00099
    t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B)
    currentOultiers = newOutliers
    t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)
    for x in newOutliers:
        currentOultiers+=[x]    
    data={}
    data["B"]=od.B
    print B 
   
    
    data["outliers"]=currentOultiers  
    data["epsilon"]=epsilon        
    pickle.dump( data, open( filename+"_INIT"+".pickle", "wb" ) )  
else:
    data  = pickle.load( open(  filename+"_INIT"+".pickle", "r" ) )  
    B = data["B"]
    currentOultiers  = data["outliers"]
    epsilon = data["epsilon"]
    od.setBInSorter(B)
    for x in currentOultiers:
        od.sorter.setOutlier(x)
    

wasDoneSomeChange = True 
iteration = 0
while wasDoneSomeChange:
    print "\n\n Iteration ",iteration 
    
    
    
      
    
    
    print "Insertion of outliers procedure    "
    print len(currentOultiers),currentOultiers

    currentOultiers, wasDoneSomeChange = od.insertOutliers_Method_CyclicAssignmentSPARSE(currentOultiers)
    print len(currentOultiers),currentOultiers
    
    misClasSamples=[]
    misClassifications = 0
    for sample in xrange(od.n):
        myLabel = od.labels[sample]
        minDistance = 100000
        closestPointID=-1
        for to in xrange(od.n):
            if to != sample:
                distance = od.sorter.computeDistanceBetweenTwoPoint(sample, to)
                if distance < minDistance:
                    minDistance = distance
                    closestPointID = to
        if myLabel != od.labels[closestPointID]:
            misClassifications=misClassifications+1
            misClasSamples+=[sample]
    print "Total Missclassifications",misClassifications,misClasSamples
    
    
    misClassifications = 0
    misClasSamples=[]
    for sample in xrange(od.n):
        myLabel = od.labels[sample]
        minDistance = 100000
        closestPointID=-1
        for to in xrange(od.n):
            if to != sample and to not in currentOultiers:
                distance = od.sorter.computeDistanceBetweenTwoPoint(sample, to)
                if distance < minDistance:
                    minDistance = distance
                    closestPointID = to
        if myLabel != od.labels[closestPointID]:
            misClassifications=misClassifications+1
            misClasSamples+=[sample]
            
    print "Total Missclassifications",misClassifications,misClasSamples
    
     
    
    
    iteration=iteration+1
    data={}
    data["B"]=B
    data["outliers"]=currentOultiers        
    pickle.dump( data, open( filename+"_"+str(iteration)+".pickle", "wb" ) ) 
    
    if iteration > 40:
        break    
    
    if (wasDoneSomeChange):
        t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)    
        print "new outliers identified",newOutliers
        for x in newOutliers:
            currentOultiers +=[x]

print "FINAL LIST OF OUTLIERS",currentOultiers

data={}
data["B"]=od.B
print od.B
data["outliers"]=currentOultiers        
pickle.dump( data, open( filename+"_"+"FINAL"+".pickle", "wb" ) )  


    
#     TODO: Bolun, please try to implement this two functions
#     outliers = insertOutliers_Method_Ri_Assignment()   
#     outliers = insertOutliers_Method_MIP_Assignment()
# 

#     if notFinished:
#         outliers = od.outliers
#         # what model do we solve to re-optimize B and D???? I am not sure about this step
#         od.setOutlierList(od.outliers)
#         t, newoutliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
#         print "we have ",len(newoutliers), "new outliers: ",newoutliers
#         outliers+=newoutliers
#         print "at the end we have ", len(outliers),":",outliers
        
    
    
    



# print t
# print "we have ",len(outliers), "outliers: ",outliers


#print "--------------------"    
#print(results)
#print(model.display())

"""
 



od.setOutlierList(outliers)
t, newoutliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
print "we have ",len(newoutliers), "outliers: ",newoutliers
outliers+=newoutliers
print "at the end we have ", len(outliers),":",outliers


data={}
data["B"]=od.B
data["outliers"]=outliers        
pickle.dump( data, open( filename+"0.pickle", "wb" ) ) 



    
    



# start adding points ....   R_i greeedy / Random insertion / MIP 







"""






