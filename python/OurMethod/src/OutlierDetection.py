from pyomo.environ import *
import numpy as np
import math
import time
#https://github.com/Pyomo/PyomoGallery/blob/master/network_interdiction/multi_commodity_flow/multi_commodity_flow_interdict.py
import mymodule
from matplotlib.mlab import dist
from dis import dis
    
EMA = 0.000001

def solveModel(model):
        opt = SolverFactory("cbc")#,solver_io='python')
#         opt = SolverFactory("cplex")
#         print "-------------Going to solve the model-------------"
#         solver_manager = SolverManagerFactory('neos')
#         results = solver_manager.solve(model, opt=opt)
        start_time = time.time()
        print "Start "
        results = opt.solve(model)#)#, warmstart=True
        elapsed_time = time.time() - start_time
        print "solving took ", elapsed_time
#         print(results)
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

    def setBInSorter(self,B):
        for i in xrange(self.d):
            for j in xrange(self.d):
                if j>i:
                    self.sorter.setBij(i,j,2*B[i,j])
                if j==i:
                    self.sorter.setBij(i,j,B[i,j])
                if j<i:
                    self.sorter.setBij(i,j,0.0)

    def __init__(self, filename ,normalize):

        self.labels = []  
        self.features = []
        f = open(filename,'rU')
        for line in f:
            data =  line.split(':')
            self.labels+=[ int(data[0]) ]
            self.features+=[  [float(xi) for xi in data[1].split() ]              ]
        f.close()
        
        #normalizeData
        if normalize:
            M = 0
            for sample in self.features:
                    normi = sum(xi*xi for xi in sample)
                    M = max(M,normi)
            M = math.sqrt(M)
            self.features = [   [ xi/M for xi in sample    ]        for sample in self.features  ]

        self.n = len(self.labels)
        self.nonOutlier = range(self.n)
        self.outlier = []
        self.d = len(self.features[0])

        self.sorter = mymodule.MySorter()
        self.sorter.InitializeData(self.n,self.d)

        for sample in xrange(self.n):
            self.sorter.setLabel(sample,self.labels[sample])
            for feat in xrange(self.d):
                self.sorter.setFeature(sample, feat,self.features[sample][feat] )


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


    def updateViolations(self):
        self.violations = self.violationsHM.values()

    def addViolation(self,n1, n2):
        hadThisKey = False
        if n1<n2:
            key = str(n1)+"_"+str(n2)
            if key in self.violationsHM:
                hadThisKey = True
            self.violationsHM[key] = [n1,n2]
        else:
            key = str(n2)+"_"+str(n1)
            if key in self.violationsHM:
                hadThisKey = True
            self.violationsHM[key] = [n2,n1]
        return hadThisKey
            
            
    def addConstraintsBetweenBandD_SPARSE(self,model):    
        def distanceBetweenPointGivenB(model, idx):
                i = self.violations[idx][0]
                j = self.violations[idx][1]
                xi = self.features[i]
                xj = self.features[j]
                x = [  (xi[k]-xj[k]) for k in xrange(self.d) ]
                return ( model.D[(idx)] ==   sum(  x[k]*x[l]* model.B[(k,l)]      for k in model.d for l in model.d   )      )
#         start_time = time.time()
        model.distanceBetweenPointGivenBConstrain = Constraint(model.S, rule=distanceBetweenPointGivenB)
#         elapsed_time = time.time() - start_time
#         print "done D contsr", elapsed_time        
            
    def addBVariable(self,model,B):    
            def fB(model, i,j):
                if i < j:
                    return (0, 0)            
                else:
                    return (None, None)
            def fBE(model, i,j):
                if i<j:
                    return 0
                if i>j:
                    return 2*B[i,j]
                return B[i,j]
            model.B = Var(model.d * model.d  ,bounds=fB, initialize=fBE ) #,bounds=(-1, 1) 
    def addDistanceVariable(self,model):    
            def fDE(model, idx):
                i = self.violations[idx][0]
                j = self.violations[idx][1]
                if j==140:
                    print idx, i,j
                distance = self.sorter.computeDistanceBetweenTwoPoint(i, j)
                if distance < 0 or distance > 1:
                    return None
                return distance
            model.D = Var(model.S, domain=NonNegativeReals, bounds=(0, 1), initialize=fDE)                         
            
    def findLargestEpsilonRowAndColumnGeneration(self):
        
        B = np.identity(self.d)
        self.setBInSorter(B)
        notDone = True
        S = {}
        
        
        
        totalPoints  = self.sorter.computeTopRiPoints(10)
        self.violationsHM={}
        for i in xrange(totalPoints):
            self.addViolation(self.sorter.getIndexForTopList(i,0) , self.sorter.getIndexForTopList(i,1))
        self.updateViolations()


        print "d = ",self.d


        
#         print self.violations
        
        
#         if True:
#             
#             start = time.time()
#             print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", self.d, self.n
#             
#             dm = [ [j,k,   sum([   (self.features[j][l]-self.features[k][l])*(self.features[j][m]-self.features[k][m]) for l in xrange(self.d) for m in xrange(self.d)           ])               ]  for j in xrange(self.n) for k in xrange(self.n)] 
# 
#             print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",time.time()-start
#             print dm[1:10]
# 
#             start = time.time()
#             for sample in self.nonOutlier:
# #                 print sample
#                 distanceInClass = 1000000
#                 distanceToOtherClass = 1000000
#                 for testTo in self.nonOutlier:
#                     if (sample <> testTo):
#                         x = [self.features[sample][k] - self.features[testTo][k] for k in xrange(self.d)]
#                         distance = sum(  x[k]*x[l]*B[k,l] for k in xrange(self.d) for l in xrange(self.d)   )
#                         if (self.labels[sample] == self.labels[testTo] and distance < distanceInClass):
#                             distanceInClass = distance
#                         if (self.labels[sample] <> self.labels[testTo] and distance < distanceToOtherClass):
#                             distanceToOtherClass = distance
#                             PI[sample] = testTo
#                 RI[sample] = distanceToOtherClass / distanceInClass
#             print "YYYYYYYYYYYYYYYYYYYYYYYYY"   ,time.time()-start          

            
        it = 0
        
        while notDone:
            it = it+1
            model = ConcreteModel()
            model.d = Set(initialize=range(self.d), doc='Set of features')
            model.S = Set(initialize=range(len(self.violations))      , doc='Set of active nodes')
            
            self.addDistanceVariable(model)
            self.addBVariable(model,B)    
            self.addConstraintsBetweenBandD_SPARSE(model)

            model.eps = Var(within=NonNegativeReals,  initialize=0) #, bounds=(0, 1)  
            def epsLessThanDij(model, idx):
                i = self.violations[idx][0]
                j = self.violations[idx][1]
                if self.labels[i] == self.labels[j]:
                    return Constraint.Skip
                else:
                    return ( model.eps <= model.D[idx]   )
            model.epsLessThanDikConstrain = Constraint(model.S, rule=epsLessThanDij)
            
            model.OBJ = Objective(expr=model.eps, sense=maximize, doc='maximize epsilon')
#             start_time = time.time()
            results = solveModel(model)
#             elapsed_time = time.time() - start_time
#             print "solving time", elapsed_time
            
            B = self.getMatrixBFromResult(model)
            self.setBInSorter(B)
            epsilon = model.eps.value
            totalPoints  = self.sorter.computeTopRiPoints(10)
            notDone = False
            for i in xrange(totalPoints):
                if (self.sorter.getValueForTopList(i) < -EMA):
                    self.addViolation(self.sorter.getIndexForTopList(i,0) , self.sorter.getIndexForTopList(i,1))
#                     print "CASE A",self.sorter.getIndexForTopList(i,0),self.sorter.getIndexForTopList(i,1),self.sorter.getValueForTopList(i)
                    notDone = True
                if (self.sorter.getValueForTopList(i) > 1+EMA):
                    self.addViolation(self.sorter.getIndexForTopList(i,0) , self.sorter.getIndexForTopList(i,1))
#                     print "CASE C",self.sorter.getIndexForTopList(i,0),self.sorter.getIndexForTopList(i,1),self.sorter.getValueForTopList(i)
                    notDone = True
                if ( (self.sorter.getValueForTopList(i) < epsilon-EMA) and (self.labels[self.sorter.getIndexForTopList(i,0)] <> self.labels[self.sorter.getIndexForTopList(i,1)]  )):
                    self.addViolation(self.sorter.getIndexForTopList(i,0) , self.sorter.getIndexForTopList(i,1))
#                     print "CASE B",self.sorter.getIndexForTopList(i,0),self.sorter.getIndexForTopList(i,1),self.sorter.getValueForTopList(i),epsilon
                    notDone = True
            self.updateViolations()
            print "Iteration ", it, " Total violations now ",len(self.violations), ' EpSILON ',epsilon
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

    def insertOutliers_Method_CyclicAssignmentSPARSE(self,  currentOultiers):
        canInsert = True
        wasDoneSomeChange = False
        while canInsert:
            canInsert = False
            for sample in currentOultiers:
                val =   self.sorter.computeRi(sample)
                if val>1:
                    canInsert = True
                    currentOultiers.remove(sample)
                    self.sorter.removeOutlier(sample)
                    wasDoneSomeChange = True
        return currentOultiers,wasDoneSomeChange



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

    def findDistanceBandSetOfOutliersForEpsilon_SPARSE(self,epsilon,Binit, currentOutliers=[]):
        
        
        self.epsilon = epsilon
        self.B = Binit
        self.violationsHM={}
        self.sorter.setEpsilon(epsilon)
        self.sorter.resetOutliers()
        
        for x in currentOutliers:
            self.sorter.setOutlier(x)
        
        
        NOTFINISHED = True
        IT=0
        TI = {}
        while NOTFINISHED:
            NOTFINISHED = False
            print "ITERATION --------",IT     
            IT=IT+1   
            self.setBInSorter(self.B)
        # we should find the worst violations for given "B"
        
            totalPoints = self.sorter.getViolationsForT()
        
            vio = [  [self.sorter.getIndexForTopList(i, 0), self.sorter.getIndexForTopList(i, 1), self.sorter.getValueForTopList(i)] for i in xrange(totalPoints)            ]
            for x in vio:
                n1=x[0]
                n2=x[1]
                TI[n1]=1
                TI[n2]=1
                hadThisKey = self.addViolation(n1, n2)
                if hadThisKey:
                    pass
                else:
                    NOTFINISHED = True
            if (NOTFINISHED):
         
                
                Ts = TI.keys()
                self.updateViolations()
                
                print "Init Itartions   total points ",totalPoints, 'TOTAL Constraints',len(self.violations), "total ts",len(Ts)
                
                model = ConcreteModel()
                model.d = Set(initialize=range(self.d), doc='Set of features')
                model.S = Set(initialize=range(len(self.violations))      , doc='Set of distance bounds')
                model.N = Set(initialize= Ts      , doc='Set of active nodes')
                
                self.addDistanceVariable(model)
                self.addBVariable(model,self.B)    
                self.addConstraintsBetweenBandD_SPARSE(model)
        
                model.t = Var(model.N, domain=NonNegativeReals, bounds=(0, 1)) #
        
                def tiBound(model, idx):
                    i = self.violations[idx][0]
                    j = self.violations[idx][1]
                    if i==j:
                        return Constraint.Skip
                    if self.labels[i] == self.labels[j]:
                        return (  model.t[(i)] <= model.D[idx] )
                    else:
                        return ( model.t[(i)] + self.epsilon <= model.D[idx]   )
                    
                model.tiBoundConstrain = Constraint( model.S , rule=tiBound)
                
                # ------------------  Objective Function        
                model.OBJ = Objective(expr=sum( model.t[i] for i in model.N ), sense=maximize, doc='maximize epsilon')
        
                results = solveModel(model)
                self.B = self.getMatrixBFromResult(model)

        t={}
        for i in model.t:
            t[i]=model.t[i].value    
        newOutliers = []
        
        
        totalPoints = self.sorter.getViolationsForT()

        for i in  xrange(totalPoints):
            sample = self.sorter.getIndexForTopList(i, 0)
            to = self.sorter.getIndexForTopList(i, 1)
            isOutlier = self.sorter.getOutlierForTopList(i)
            if isOutlier ==1:
                newOutliers+=[sample]
            
        print "total points from C++",totalPoints, len(vio)




        
#         for idx in model.S:
#                 print model.D[idx].value, self.violations[idx][0],self.violations[idx][1],self.sorter.computeDistanceBetweenTwoPoint(self.violations[idx][0], self.violations[idx][1])
                


        return t,  newOutliers, self.B


        

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
