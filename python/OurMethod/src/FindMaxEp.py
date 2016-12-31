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
    
    model.I = range(n)
    
    model.J = range(n)
    
    model.p = range(dimension)
    # Define Matix Delta
    model.Delta = [0]*n  
    for i in xrange(n):  
        model.Delta[i] = [0]*n  
  
    for i in xrange(n):  
        for j in xrange(n):  
            model.Delta[i][j] = [0]*dimension
        
    for i in xrange(n):  
        for j in xrange(n): 
            for p in xrange(dimension): 
                model.Delta[i][j][p]= features[i][p]-features[j][p]
    
    # Define Matix B
    model.B = [0]*dimension  
    for i in xrange(dimension):  
        model.B[i] = [0]*dimension  
  
    for i in xrange(dimension):
        for j in xrange(dimension):
            model.B[i][j] = Var(within=Reals, initialize=0)

    # Define Distance[i,j]
    model.d = [0]*n  
    for i in xrange(n):  
        model.d[i] = [0]*n  
    for i in xrange(n):
        for j in xrange(n):
            model.d[i][j] = Var(within=NonNegativeReals,bounds=(0,1))
   
    model.Epsilon = Var(within=NonNegativeReals, bounds=(0,1), initialize=0)

    model.OBJ = model.Epsilon
 



    # this is constraint (11b)
    for i in xrange(n):
        myLabel = labels[i]
        for k in xrange(n):
            if (i != k) and(labels[k] != myLabel) :
                model.Constraint_11b[i,k] = Constraint(expr =  model.Epsilon <= model.d[i][k])
            else:
                model.Constraint_11b[i,k] = Constraint(expr =  0 <= 0)
                
    # this is constraint (8b)   
    def constraint_8b_rule(model,i,j):
        # create lists for loop in expression of constraints
        model.sum_21=range(dimension-1) 
        model.sum_22=range(dimension-1) 
        for i in xrange(dimension-1):  
            model.sum_22[i] = [] 
        for k1 in xrange(dimension-1):  
            for k2 in xrange(dimension-k1-1):
                temp=k2+k1+1
                model.sum_22[k1].append(temp)
        # return the expression for the constraint for d[i,j]
        return sum(model.Delta[i][j][k] * model.Delta[i][j][k] * model.B[k][k] for k in model.p)\
         + 2*sum(sum(model.Delta[i][j][k]*model.Delta[i][j][l]* model.B[k][l]) for l in model.sum_22[k]) for k in model.sum_21)\
         == model.d[i][j]
    # the next line creates one constraint for each member of the set model.I and Set model.J
    model.Constraint_8b = Constraint(model.I,model.J,rule=constraint_8b_rule)

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
