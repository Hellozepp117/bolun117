
import matplotlib.pyplot as plt

 


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from OutlierDetection import OutlierDetection
from matplotlib.mlab import dist
import pickle 
n_neighbors = 1

# import some data to play with


filename = "syntheticNoOutliers.txt"
filename = "syntheticWithOutliers.txt"

# filename = 'synthetic.txt'

# data  = pickle.load( open(   filename+"_FINAL"+".pickle", "r" ) )     

data  = pickle.load( open(   filename+"_INIT"+".pickle", "r" ) )     

filenameL=filename.replace(".", "_")#+"I2"


B = data['B']

print B



asfdsafsafa

 
outliers = data['outliers']
print outliers 
# outliers=[]

od = OutlierDetection(filename , True)    

 
 
 
 
X =  od.features
y =  od.labels

for l in xrange(3):
    xx=[]
    yy=[]
    for i in xrange(len(y)):
        if y[i]==l:
            xx+=[ X[i][0] ]
            yy+=[ X[i][1] ]
#    plt.plot(xx, yy, '.')

#plt.axis('equal')
#plt.show()




h = .005  # step size in the mesh
# h=0.05
# h=0.01
# h=0.1
# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])


X = np.array(X)

w, hh = plt.figaspect(1.)
#   fig = Figure(figsize=(w,h))
fi = plt.figure(figsize=(w,hh))

    
    # Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)

print y

plt.show()

filename="../../../../2017_MSC_Bolun_ICML2017/fig/"+filenameL+"_"+".eps"
fi.savefig(filename)




for weights in [3]:# xrange(3):
    # we create an instance of Neighbours Classifier and fit the data.
#    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
#    clf.fit(X, y)


 

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = -1.1,  1.1
    y_min, y_max = -1.1,  1.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    
    xv = xx.ravel()
    yv = yy.ravel()
    
    
    Z = []
    for xi, yi in zip(xv,yv):
        
        minDistance = 10000
        minClass = -1
        
        for i in xrange(len(y)):
            x=X[i]
            
            if weights==0:
                distance = (x[0]-xi)**2+(x[1]-yi)**2
            if weights==1:
                distance = max( (x[0]-xi)**2 , (x[1]-yi)**2 )
            if weights==2:
                distance = abs(x[0]-xi) +abs(x[1]-yi) 
            if weights==3:
                if i in outliers:
                    continue
                distance = B[0,0]*(x[0]-xi)**2+B[1,1]*(x[1]-yi)**2 + 2*B[0,1]*(x[1]-yi)*(x[0]-xi)
                
                
                
            if distance < minDistance:
                minDistance=distance
                minClass = y[i]
        
        
        
        Z+=[minClass]
        
    Z=np.array(Z)   
        
    
    

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    fi = plt.figure(figsize=(w,hh))
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
    
    
    if weights==3:
        cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF','#000000','#000000','#000000'])

        for j in xrange(len(y)):
            if j in outliers:
                y[j]=y[j]+3
        print y
    
    
    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    

    print "XXX"

    if weights==0:
        plt.title("Euclidean Norm")
    if weights==1:
        plt.title("Maximum Norm")
    if weights==2:
        plt.title("Manhattan Norm")

    if weights==3:
        plt.title("B Norm")
    plt.axis('equal')
    plt.show()
    
    filename="../../../../2017_MSC_Bolun_ICML2017/fig/"+filenameL+"_"+str(weights)+".eps"
    fi.savefig(filename)


    
    #plt.xlim(xx.min(), xx.max())
    #plt.ylim(yy.min(), yy.max())
    #plt.title("3-Class classification (k = %i, weights = '%s')"
    #          % (n_neighbors, weights))
