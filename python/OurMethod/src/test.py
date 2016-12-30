'''


@author: Bolun
'''
labels = [ 0, 0, 1, 1]
features = [ [0, 1],[.1, 1.1 ],[.1, 2.1 ],[-2, 2.01 ] ]
dimension = len(features[0])
    
print dimension
print features[1][0]

for i in xrange(0,dimension):
    print i
    
    def c11bRule(model,labels,i,k):
    n = len(labels)
    for i in xrange(n):
        myLabel = labels[i]
        for k in xrange(n):
            if labels[k] != myLabel:
                return 0 <= 0
            
    return model.x[i,k,v] <= model.a[i,k]*model.y[i]