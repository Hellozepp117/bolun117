

import matplotlib.pyplot as plt
import numpy as np

asfsafa
# f = open("syntheticNoOutliers.txt","w")
f = open("syntheticWithOutliers.txt","w")



cov = [[1.1, -0.9999], [-0.9999, 1.1]]  # diagonal covariance
cmap_bold = ['#FF0000', '#00FF00', '#0000FF']

c=10
N=50 
fi = plt.figure()
mean = [0, 0]
x, y = np.random.multivariate_normal(mean, cov, N).T
plt.plot(x, y, 'x' )

for i,j in zip(x,y):
    f.write("0:"+str(i)+" "+str(j)+"\n")


mean = [15/c, 10/c]
xx, yy = np.random.multivariate_normal(mean, cov, N).T
plt.plot(xx, yy, '<')
for i,j in zip(xx,yy):
    f.write("1:"+str(i)+" "+str(j)+"\n")

mean = [-10/c, -10/c]
xxx, yyy = np.random.multivariate_normal(mean, cov, N).T

for i,j in zip(xxx,yyy):
    f.write("2:"+str(i)+" "+str(j)+"\n")

plt.plot(xxx, yyy, '.')


mean = [25/c, 25/c]
x4, y4= np.random.multivariate_normal(mean, cov, N).T
plt.plot(x4, y4, 'x')

for i,j in zip(x4,y4):
    f.write("0:"+str(i)+" "+str(j)+"\n")





plt.axis('equal')
plt.show()

filename="../../../icml2017/fig/synthetic_withOutliers.eps"
fi.savefig(filename)

     
f.close()
