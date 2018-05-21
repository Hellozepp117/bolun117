param n>=0, integer;
param m>=0, integer;


set I =1..n ;
set J =1..m ;

var x  {j in J}         , binary ;
var y  {i in I, j in J}  >=0     ;
var z  {j in J}         , binary ;


param f {J}                      ;
param h {I}                      ;
param c {i in I, j in J}         ;
param a                          ;
param d {j in J}                 ;

subject to oneplace {i in I}         : sum{j in J} y[i,j]    =  1                      ;
subject to logic    {i in I, j in J} : x[j]  >=  y[i,j]                                ;
subject to capacity {j in J}         : sum {i in I} h[i] * y[i,j] <= 200000 + a * z[j] ;



minimize cost: sum {j in J} f[j] * x[j] + sum {i in I, j in J} c[i,j] * h[i] * y[i,j] + sum {j in J} z[j] * d[j] ;