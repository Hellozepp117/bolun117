'''


@author: Bolun
'''
labels = [ 0, 0, 1, 1]
features = [ [0, 1],[.1, 1.1 ],[.1, 2.1 ],[-2, 2.01 ] ]
dimension = len(features[0])
    
print dimension
print features[1][0]

J=range(len(labels))

print J

p=5
P_1=range(p) 
P_2=range(p-1) 
for i in xrange(p-1):  
    P_2[i] = [] 
for k1 in xrange(p-1):  
    for k2 in xrange(p-k1-1):
        temp=k2+k1+1
        P_2[k1].append(temp)
print P_2