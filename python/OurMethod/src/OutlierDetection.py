from pyomo.environ import *
import numpy as np
import math
import time
#https://github.com/Pyomo/PyomoGallery/blob/master/network_interdiction/multi_commodity_flow/multi_commodity_flow_interdict.py

    

def solveModel(model):
        opt = SolverFactory("cplex")
        
#         print "-------------Going to solve the model-------------"
#         solver_manager = SolverManagerFactory('neos')
#         results = solver_manager.solve(model, opt=opt)
        
        results = opt.solve(model)
        print(results)
#         print "-------------Model solved-------------"
        
        return results




class OutlierDetection:

    EPS_M = 0.000001
    def getMatrixDFromResult(self,model):
        D=np.zeros((self.n, self.n))
        for i in model.NAll:
            for j in model.NAll:
                D[i,j] = model.D[(i,j)].value
        return D



    def getMatrixBFromResult(self,model):
        B=np.zeros((self.d, self.d))
        for i in model.d:
            for j in model.d:
                if i==j:
                    B[i,j] = model.B[(i,j)].value
                if i>j:
                    B[i,j] =0.5* model.B[(i,j)].value    
                    B[j,i] = B[i,j]
        return B

    


    def __init__(self, filename ,normalize):

        self.labels = []  
        self.features = []
        f = open(filename,'rU')
        for line in f:
            data =  line.split(':')
            self.labels+=[ int(data[0]) ]
            self.features+=[  [float(xi) for xi in data[1].split() ]              ]
        f.close()
        #centralize data TODO    
            
        #normalizeData
        if normalize:
            M = 0
            for sample in self.features:
                    normi = sum(xi*xi for xi in sample)
                    M = max(M,normi)
            M = math.sqrt(M)
            self.features = [   [ xi/M for xi in sample  ]        for sample in self.features  ]

        self.n = len(self.labels)
        self.nonOutlier = range(self.n)
        self.outlier = []
        self.d = len(self.features[0])


    def addConstraint_d_ij_as_function_of_features_and_B(self,model):
        #relation between B and D
        def distanceBetweenPointGivenB(model, i,j):
            xi = self.features[i]
            xj = self.features[j]
            x = [  (xi[k]-xj[k]) for k in xrange(self.d) ]
            return ( model.D[(i,j)] ==   sum(  x[k]*x[l]* model.B[(k,l)]      for k in model.d for l in model.d   )      )
        
        start_time = time.time()
        print "Start "
        model.distanceBetweenPointGivenBConstrain = Constraint(model.NAll*model.NAll, rule=distanceBetweenPointGivenB)
        elapsed_time = time.time() - start_time
        print "done D contsr", elapsed_time
    def addConstraint_lower_diagonal_of_B_is_zero(self,model):
        #matrix B will be zero under diagonal
        def lowerBisZero(model, i,j):
            if i >= j:
                return Constraint.Skip
            else:
                return ( model.B[(i,j)] == 0   )
        model.lowerBisZeroConstrain = Constraint(model.d*model.d, rule=lowerBisZero)


    def findLargestEpsilon(self):
        
        model = ConcreteModel()
        # ------------------  definition of sets
        model.N = Set(initialize=self.nonOutlier, doc='Set of nodes')
        model.NAll = Set(initialize=range(self.n), doc='Set of nodes')
        model.d = Set(initialize=range(self.d), doc='Set of features')        
        # ------------------  definition of variables        
        model.D = Var(model.NAll * model.NAll, domain=NonNegativeReals, bounds=(0, 1)) 
        model.eps = Var(within=NonNegativeReals,  initialize=0) #bounds=(0, 1),
        model.B = Var(model.d * model.d   ) #,bounds=(-1, 1) 
        # ------------------  Constraints        
        def epsLessThanDij(model, i,j):
            if self.labels[i] == self.labels[j]:
                return Constraint.Skip
            else:
                return ( model.eps <= model.D[(i,j)]   )
        model.epsLessThanDikConstrain = Constraint(model.N*model.N, rule=epsLessThanDij)
        self.addConstraint_lower_diagonal_of_B_is_zero(model)
        self.addConstraint_d_ij_as_function_of_features_and_B(model)
        # ------------------  Objective Function        
        model.OBJ = Objective(expr=model.eps, sense=maximize, doc='maximize epsilon')
        # ------------------  Solve Problem        
        results = solveModel(model)
        B = self.getMatrixBFromResult(model)
        D = self.getMatrixDFromResult(model)
        return model.eps.value, B, D, results, model


    def setOutlierList(self,outliers):
        self.nonOutlier=range(self.n)
        
        for outlier in outliers:
            self.nonOutlier.remove(outlier)
        self.outliers = outliers



    def insertOutliers_Method_CyclicAssignment(self):
        didSomeInsertion = False
        notFinished = True
        while notFinished:
            notFinished = False
            for outlier in self.outliers:
                minDistance = 100000
                minDistanceLabel = -1
                # find that if the closes point is the same class
                for trialPoint in self.nonOutlier:
                    if minDistance > self.D[outlier,trialPoint]:
                        minDistance = self.D[outlier,trialPoint]
                        minDistanceLabel = self.labels[trialPoint]
                if minDistanceLabel == self.labels[outlier]:
                    self.outliers.remove(outlier)
                    self.nonOutlier+=[outlier]
                    didSomeInsertion = True
                    notFinished = True
                    break
        return didSomeInsertion
                        
                
                
                
                
                
                
                
                
                
                
                
        
        
        
        
        
        
    def insertOutliers_Method_Ri_Assignment(self):
        pass
        
    def insertOutliers_Method_MIP_Assignment(self):
        pass

        

    def findDistanceBandSetOfOutliersForEpsilon(self,epsilon):
        self.epsilon = epsilon
        model = ConcreteModel()
        # ------------------  definition of sets        
        model.N = Set(initialize=self.nonOutlier, doc='Set of nodes')
        model.NAll = Set(initialize=range(self.n), doc='Set of nodes')
        model.d = Set(initialize=range(self.d), doc='Set of features')        
        # ------------------  definition of variables        
        model.D = Var(model.NAll * model.NAll, domain=NonNegativeReals, bounds=(0, 1)) 
        model.B = Var(model.d * model.d   ) #,bounds=(-1, 1) 
        model.t = Var(model.N, domain=NonNegativeReals, bounds=(0, None)) 
        # ------------------  Constraints        
        def tiBound(model, i,j):
            if i==j:
                return Constraint.Skip
            if self.labels[i] == self.labels[j]:
                return (  model.t[(i)] <= model.D[(i,j)] )
            else:
                return ( model.t[(i)] + self.epsilon <= model.D[(i,j)]   )
        model.tiBoundConstrain = Constraint(model.N*model.N, rule=tiBound)
        self.addConstraint_lower_diagonal_of_B_is_zero(model)
        self.addConstraint_d_ij_as_function_of_features_and_B(model)
        # ------------------  Objective Function        
        model.OBJ = Objective(expr=sum( model.t[i] for i in model.N ), sense=maximize, doc='maximize epsilon')

        # ------------------  Solve Problem        
        results = solveModel(model)
        
        self.B = self.getMatrixBFromResult(model)
        self.D = self.getMatrixDFromResult(model)
        
        t=np.zeros(( self.n))
        for i in model.N:
            t[i] = model.t[(i)].value
        outliers=[]
#         for i in xrange(self.n):
#             m = 1000;
#             for j in xrange(self.n):
#                 if  self.labels[i]==self.labels[j] and i<>j:
#                     m = min(m, self.D[i,j])
#             if m > t[i]+self.EPS_M:
#                 outliers+=[i]  

        
 
        
        minPoint = -1
        for sample in model.N: 
            minDistanceInClass=10000
            minDistanceToOtherClass = 10000              
            for toTest in model.N:
                if (sample <> toTest):
                    if self.labels[sample]==self.labels[toTest] and self.D[sample,toTest] <   minDistanceInClass:
                        minDistanceInClass =  self.D[sample,toTest]
                    if self.labels[sample] <> self.labels[toTest] and self.D[sample,toTest] <   minDistanceToOtherClass:
                        minDistanceToOtherClass =  self.D[sample,toTest]
                        minPoint = toTest
                        
                        
                        
            if (minDistanceToOtherClass < minDistanceInClass):
                outliers+=[sample] 
#                 print "adding outlier",sample,"closes point is ",minPoint           
                
                
        return  t, outliers, results, model
