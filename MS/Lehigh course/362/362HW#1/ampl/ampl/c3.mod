param n>=0, integer;
param m>=0, integer;

set I =1..n ;
set J =1..m ;

var x {j in J}, binary;
var y {i in I, j in J} >=0;

param f  {j in J};
param co {i in I, j in J};
param p  {j in J};
param h  {i in I};
param ca {j in J};

subject to demandsayisfy {i in I}: sum {j in J} y[i,j] = 1;
subject to facilityopen  {i in I, j in J}: x[j]>=y[i,j];
subject to capacity {j in J}: sum { i in I} h[i]* y[i,j] <= ca[j];


minimize cost: sum {j in  J} f[j] * x[j] + sum{i in I, j in J} ( co[i,j] + p[j] ) * h[i] * y[i,j];