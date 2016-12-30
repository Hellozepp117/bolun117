'''
Created 

@author: Bolun
'''
from __future__ import division
from pyomo.environ import *

def loadData(filename):
    labels = [0, 0,  1, 1]  
    features = [ [0, 1],[.1, 0.8 ],[.1, -.9 ],[-0.2, 0.01 ] ]
    return labels, features  


def createModelForFidingEpMax(labels, features):
    
    model = ConcreteModel()

    dimension = len(features[0])
    
    n = len(labels)
    
    # Define Matix B
    for i in xrange(dimension):
        for j in xrange(dimension):
            model.B[i][j] = Var(within=Reals, initialize=0)
            
    # Define Distance[i,j]
    for i in xrange(n):
        for j in xrange(n):
            model.d[i,j] = Var(within=NonNegativeReals,bounds=(0,1))
   
    model.Epsilon = Var(within=NonNegativeReals, bounds=(0,1), initialize=0)

    model.OBJ = model.Epsilon
 



    # this is constraint (11b)
    for i in xrange(n):
        myLabel = labels[i]
        for k in xrange(n):
            if (i != k) and(labels[k] != myLabel) :
                model.Constraint11b[i,k] = Constraint(expr =  model.Epsilon <= model.d[i,k])
            else:
                model.Constraint11b[i,k] = Constraint(expr =  0 <= 0)
                
    # this is constraint (8b)                
    for i in xrange(n):
        for j in xrange(n):
                model.Constraint11b[i,j] = Constraint(expr =  model.Epsilon <= model.d[i,k])

    
        
        
        


    
    return model


def test(labels, features):
 
 
 
 
    model = createModelForFidingEpMax(labels, features)

 


    opt = SolverFactory("cplex")
    solver_manager = SolverManagerFactory('neos')
    results = solver_manager.solve(model,opt=opt)


    print(results)


    print(model.display())
    
    print "-------------------"
    
labels, features = loadData("doesnt matter")    
test(labels, features)
