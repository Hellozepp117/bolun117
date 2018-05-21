#Model

set S = 1..7;

set T = 1..7;

set R = 2..6;

param c{S,T};

param a{S,T};

var x{S,T} >= 0;

minimize ShortestPath: sum{i in S, j in T} c[i,j] * x[i,j];

Con{i in R}: sum {j in T} a[i,j] * x[i,j] = sum {j in T} a[j,i] * x[j,i];

Con1: sum {j in T} a[1,j] * x[1,j] = 1 + sum {j in T} a[j,1] * x[j,1];

Con7: sum {j in T} a[7,j] * x[7,j] = -1 + sum {j in T} a[j,7] * x[j,7];

option solver cplex;





