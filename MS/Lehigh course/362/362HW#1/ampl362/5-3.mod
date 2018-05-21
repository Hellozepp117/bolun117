#Model

set S = 1..5;

set T = 1..5;

set R = 1..2;

param a{R,T};

param b{S,T};

param c{S};

var x{S,T} >= 0;

var y{R,T} >= 0 , binary;

minimize Cost: sum {i in R, j in T} a[i,j] * y[i,j] + sum{i in S, j in T} b[i,j] * x[i,j];

Logic{j in T}: y[1,j] + y[2,j] <= 1;

Capacity{j in T}: sum {i in S} x[i,j] <= y[1,j] * 200000 + y[2,j]*400000;

Demand {i in S} : sum {j in T} x[i,j] >= c[i];

option solver cplex;





