from __future__ import division

from OutlierDetection import *





# od = OutlierDetection('dataset3.txt2' , True)    
od = OutlierDetection('50_c2_d2.txt' , False)    


epsilonMax, B, D, results, model = od.findLargestEpsilon()

print "Epsilon max = ", epsilonMax
# print 'Matrix B is \n', B
# print "Matrix D is  \n ", D

#print "--------------------"    
#print(results)
#print(model.display())

 
epsilon = epsilonMax*0.5
t, outliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
print "we have ",len(outliers), "outliers: ",outliers


notFinished = True
iteration = 0
while notFinished:
    # remove outliers and resolve
    
    print "\n\n Iteration ",iteration 
    
    od.setOutlierList(outliers)
    print od.outliers
    print od.nonOutlier
    notFinished = od.insertOutliers_Method_CyclicAssignment()
#     TODO: Bolun, please try to implement this two functions
#     outliers = insertOutliers_Method_Ri_Assignment()   
#     outliers = insertOutliers_Method_MIP_Assignment()

    print od.outliers
    print od.nonOutlier

#     if notFinished:
#         # what model do we solve to re-optimize B and D???? I am not sure about this step
#         print od.B
#         epsilonMax, B, D, results, model = od.findLargestEpsilon()
#         print "Epsilon max = ", epsilonMax
#         epsilon = epsilonMax*0.5
#         t, outliersNEW, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
#         outliers+=outliersNEW
#         print "we have ",len(outliersNEW), "outliers: ",outliersNEW
#         print "all outliers ",len(outliers)," : ",outliers
#         print od.B
    
    iteration=iteration+1
    
    
    



# start adding points ....   R_i greeedy / Random insertion / MIP 














