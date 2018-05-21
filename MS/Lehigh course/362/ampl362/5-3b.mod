#Model

set S = 1..5;

set T = 1..5;

param a{S,T};

param p{S};

param c{S};

param d{T};

var x{S,T} >= 0;

var y{S} , binary;

minimize Cost: sum {i in S, j in T} a[i,j] * x[i,j] + sum{i in S} p[i] * ( sum{j in T} x[i,j]);

Demand {j in T} : sum {i in S} x[i,j] >= d[j];

option solver cplex;





