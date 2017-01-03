from __future__ import division

from OutlierDetection import *





od = OutlierDetection('dataset2.txt' )    

epsilonMax, B, D, results, model = od.findLargestEpsilon()

print "Epsilon max = ", epsilonMax
print 'Matrix B is \n', B
print "Matrix D is  \n ", D

#print "--------------------"    
#print(results)
#print(model.display())

 
epsilon = epsilonMax*0.5
B, D,t, outliers, results, model = od.findDistanceBandSetOfOutliersForEpsilon(epsilon)
print 'Matrix B is \n', B
print "Matrix D is  \n ", D
print "vector t is  \n ", t
print "outliers: ",outliers



