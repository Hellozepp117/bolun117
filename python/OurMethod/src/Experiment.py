from __future__ import division

from OutlierDetection import *

import pickle 
# filename = 'dataset_cifar2_sub2.txt'
# od = OutlierDetection('50_c2_d2.txt' , False)    



# filename = 'dataset3.txt'
filename = 'dataset_cifar2.txt'
# filename = 'dataset_cifar_sub.txt'
# filename = 'dataset_cifar2_sub.txt'
filename = '50_c2_d2.txt'

od = OutlierDetection(filename , True)    



epsilonMax, B = od.findLargestEpsilonRowAndColumnGeneration()

print "Epsilon max = ", epsilonMax

# od.setBInSorter(B)


# epsilonMax, B, D, results, model = od.findLargestEpsilon()

# for i in xrange(od.n):
#     for j in xrange(od.n):
#         print i,j, od.sorter.computeDistanceBetweenTwoPoint(i, j), D[(i,j)]
# print "Epsilon max = ", epsilonMax
# print B



# print 'Matrix B is \n', B
# print "Matrix D is  \n ", D

#print "--------------------"    
#print(results)
#print(model.display())

"""
 
epsilon = epsilonMax*0.01
t, outliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
print "we have ",len(outliers), "outliers: ",outliers



od.setOutlierList(outliers)
t, newoutliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
print "we have ",len(newoutliers), "outliers: ",newoutliers
outliers+=newoutliers
print "at the end we have ", len(outliers),":",outliers


data={}
data["B"]=od.B
data["outliers"]=outliers        
pickle.dump( data, open( filename+"0.pickle", "wb" ) ) 


notFinished = True 
iteration = 0
while notFinished:
    # remove outliers and resolve
    print "\n\n Iteration ",iteration 
    
   
    od.setOutlierList(outliers)
    print od.outliers
    print od.nonOutlier
    print "Insertion of outliers procedure    "
    notFinished = od.insertOutliers_Method_CyclicAssignment()
#     TODO: Bolun, please try to implement this two functions
#     outliers = insertOutliers_Method_Ri_Assignment()   
#     outliers = insertOutliers_Method_MIP_Assignment()

    print od.outliers
    print od.nonOutlier

    if notFinished:
        outliers = od.outliers
        # what model do we solve to re-optimize B and D???? I am not sure about this step
        od.setOutlierList(od.outliers)
        t, newoutliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
        print "we have ",len(newoutliers), "new outliers: ",newoutliers
        outliers+=newoutliers
        print "at the end we have ", len(outliers),":",outliers
        
    
    data={}
    data["B"]=od.B
    data["outliers"]=outliers        
    pickle.dump( data, open( filename+str(iteration)+".pickle", "wb" ) ) 
    
    iteration=iteration+1
    
    
    



# start adding points ....   R_i greeedy / Random insertion / MIP 







"""






