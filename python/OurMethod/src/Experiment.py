from __future__ import division

from OutlierDetection import *





# od = OutlierDetection('dataset3.txt2' , True)    
od = OutlierDetection('50_c2_d2.txt' , False)    


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


# remove outliers and resolve

# start adding points ....  MIP / R_i greeedy / Random insertion














