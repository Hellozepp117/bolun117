import mymodule
import numpy as np

n=10
d=3

X = np.random.rand(n,d)
labels = np.random.rand(n,1)
labels = [ int(x < 0.5) for x in labels]
print labels


sorter = mymodule.MySorter()
sorter.InitializeData(n,d)


print X
B=np.random.rand(d,d)
for i in xrange(d):
	for j in xrange(d):
		if j< i:
			B[i,j] = 0
print B










sorter.MethodB()
sorter.MethodB(10)
print sorter.GetValA()
