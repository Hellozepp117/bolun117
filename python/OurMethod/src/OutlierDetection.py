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
        print "INIT FINISHED"


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



    def findLargestEpsilonRowAndColumnGeneration(self):
        
        B = np.identity(self.d)
        notDone = True
        S = {}
        
        if True:
            RI = {}
            PI = {}
            # Now let's use current Metric to find out critical points
            
            start = time.time()
            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            
            dm = [ [j,k,   sum([   (self.features[j][l]-self.features[k][l])*(self.features[j][m]-self.features[k][m]) for l in xrange(self.d) for m in xrange(self.d)           ])               ]  for j in xrange(self.n) for k in xrange(self.n)] 

            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",time.time()-start
            print dm[1:10]

            start = time.time()
            for sample in self.nonOutlier:
#                 print sample
                distanceInClass = 1000000
                distanceToOtherClass = 1000000
                for testTo in self.nonOutlier:
                    if (sample <> testTo):
                        x = [self.features[sample][k] - self.features[testTo][k] for k in xrange(self.d)]
                        distance = sum(  x[k]*x[l]*B[k,l] for k in xrange(self.d) for l in xrange(self.d)   )
                        if (self.labels[sample] == self.labels[testTo] and distance < distanceInClass):
                            distanceInClass = distance
                        if (self.labels[sample] <> self.labels[testTo] and distance < distanceToOtherClass):
                            distanceToOtherClass = distance
                            PI[sample] = testTo
                RI[sample] = distanceToOtherClass / distanceInClass
            print "YYYYYYYYYYYYYYYYYYYYYYYYY"   ,time.time()-start          
            M = 0
            Mi = -1
            for k in RI:
                if  RI[k] > 3:
                    S[k] = 1
                    S[PI[k]] = 1 
            print "RI:",RI
            
        
        
        while notDone:
            
        
            model = ConcreteModel()
            # ------------------  definition of sets
            model.N = Set(initialize=self.nonOutlier, doc='Set of nodes')
            model.NAll = Set(initialize=range(self.n), doc='Set of nodes')
            model.d = Set(initialize=range(self.d), doc='Set of features')        
            
            
            model.S = Set(initialize=S.keys(), doc='Set of active nodes')
            
            model.D = Var(model.S * model.S, domain=NonNegativeReals, bounds=(0, 1)) 
            model.eps = Var(within=NonNegativeReals,  initialize=0) #bounds=(0, 1),
            model.B = Var(model.d * model.d   ) #,bounds=(-1, 1) 
            
            def epsLessThanDij(model, i,j):
                if self.labels[i] == self.labels[j]:
                    return Constraint.Skip
                else:
                    return ( model.eps <= model.D[(i,j)]   )
            model.epsLessThanDikConstrain = Constraint(model.S*model.S, rule=epsLessThanDij)
            
            self.addConstraint_lower_diagonal_of_B_is_zero(model)
            
            def distanceBetweenPointGivenB(model, i,j):
                xi = self.features[i]
                xj = self.features[j]
                x = [  (xi[k]-xj[k]) for k in xrange(self.d) ]
                return ( model.D[(i,j)] ==   sum(  x[k]*x[l]* model.B[(k,l)]      for k in model.d for l in model.d   )      )
            
            start_time = time.time()
            print "Start "
            model.distanceBetweenPointGivenBConstrain = Constraint(model.S*model.S, rule=distanceBetweenPointGivenB)
            elapsed_time = time.time() - start_time
            print "done D contsr", elapsed_time

            model.OBJ = Objective(expr=model.eps, sense=maximize, doc='maximize epsilon')
            
            results = solveModel(model)
            B = self.getMatrixBFromResult(model)

            epsilon = model.eps.value


            notDone = False
            print S.keys()            
            # CHECK ALL CONSTRAINTS
            smallest = 10000
            largest = -10000
            epsSmallest = 100000
            smAdd = []
            larAdd = []
            epsAdd = []
            for sample in model.N:
                for testTo in model.N:
                    if (sample <> testTo):
                        x = [self.features[sample][k] - self.features[testTo][k] for k in xrange(self.d)]
                        distance = sum(  x[k]*x[l]*B[k,l] for k in xrange(self.d) for l in xrange(self.d)   )
                        if (self.labels[sample] == self.labels[testTo] ):
                            if distance < 0 and distance < smallest:
                                smallest = distance
                                smAdd = [sample, testTo]
                                notDone = True
#                                 print "PROBLEM1", sample, testTo
                            if distance > 1 and distance > largest:
                                largest = distance
                                larAdd = [sample, testTo]
                                notDone = True
#                                 print "PROBLEM2", sample, testTo
                                
                        if (self.labels[sample] <> self.labels[testTo] ):
                            if distance < epsilon:
#                                 print "PROBLEM3", sample, testTo,epsSmallest,distance, epsAdd
                                
                                notDone = True
                                if distance < epsSmallest:
                                    epsSmallest = distance
                                    epsAdd= [sample, testTo]
            for e in smAdd:
                S[e]=1
            for e in larAdd:
                S[e]=1
            for e in epsAdd:
                S[e]=1
            
                            
            print S.keys()
            print len(S.keys()), self.n
            
            
        
        
        
        
        # ------------------  definition of variables        
        # ------------------  Constraints        
        # ------------------  Objective Function        
        # ------------------  Solve Problem        
#         D = self.getMatrixDFromResult(model)
        return model.eps.value , B


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
        model.epsLessThanDikConstrain = Constraint(model.NAll*model.NAll, rule=epsLessThanDij)
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
