#Model

param np;


param nr;


set P = 1..np;


set R = 1..nr;


param maxCap {P};


param demand {R};


param cost {P,R};


var x {P,R} >= 0;


#option solver cplex;


#Objective function

minimize tcost: sum {i in P, j in R} cost[i,j] * x[i,j];


#Cons1
subject to capCon {i in P}: sum {j in R} x [i,j] <= maxCap [i];


#Cons2
subject to demCon {j in R}: sum {i in P} x [i,j] >= demand [j];