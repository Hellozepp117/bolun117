from __future__ import division
from pyomo.environ import *


def createDefaultModel():
	model = ConcreteModel()

	model.x = Var([1,2], domain=NonNegativeReals)

	model.OBJ = Objective(expr = model.x[1] + model.x[2])
	
	return model
 




for j in xrange(20):

	model = createDefaultModel()

	model.Constraint1 = Constraint(expr =  model.x[1] * model.x[2] >= 1)

	opt = SolverFactory("cplex")

	results = opt.solve(model)


	print(results)

	print "-------------------"
	print(model.x.display())
	print "-------------------"

 
print(model.display())

print "-------------------"


for j in model.x:
 
	print model.x[j].value




