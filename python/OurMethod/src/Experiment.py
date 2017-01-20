from __future__ import division

from OutlierDetection import *

import pickle 




filename = 'dataset_cifar2_sub2.txt'
od = OutlierDetection('50_c2_d2.txt' , False)    



# filename = 'MNIST.txt'
# filename = 'CIFAR.txt'
# filename = 'dataset_cifar2.txt'
# filename = 'dataset_cifar_sub.txt'
# filename = 'dataset_cifar2_sub.txt'
# od = OutlierDetection(filename , True)    




# filename = '50_c2_d2.txt'
# od = OutlierDetection(filename , False)    




epsilonMax, B = od.findLargestEpsilonRowAndColumnGeneration()

print "Epsilon max = ", epsilonMax

epsilon = epsilonMax*0.01


t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B)
currentOultiers = newOutliers
t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)
for x in newOutliers:
    currentOultiers+=[x]

data={}
data["B"]=od.B
data["outliers"]=currentOultiers  
data["epsilon"]=epsilon        
pickle.dump( data, open( filename+"_INIT"+".pickle", "wb" ) )  

wasDoneSomeChange = True 
iteration = 0
while wasDoneSomeChange:
    print "\n\n Iteration ",iteration 
    
    print "Insertion of outliers procedure    "
    print currentOultiers

    currentOultiers, wasDoneSomeChange = od.insertOutliers_Method_CyclicAssignmentSPARSE(currentOultiers)
    print currentOultiers
    
    if (wasDoneSomeChange):
        t,  newOutliers, B = od.findDistanceBandSetOfOutliersForEpsilon_SPARSE(epsilon,B,currentOultiers)    
        print newOutliers
        for x in newOutliers:
            currentOultiers +=[x]
    if iteration > 4:
        break
    iteration=iteration+1
    data={}
    data["B"]=od.B
    data["outliers"]=currentOultiers        
    pickle.dump( data, open( filename+"_"+str(iteration)+".pickle", "wb" ) ) 
    
print "FINAL LIST OF OUTLIERS",currentOultiers





    
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






