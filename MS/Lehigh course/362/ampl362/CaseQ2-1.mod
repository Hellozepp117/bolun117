#Model

set S = 1..4;

set T = 1..6;

param c1{S};

param c2{S};

param d1{T};

param d2{T};

param a{S,T};

param f1{S};

param f2{S};

var p{S}>= 0 , integer;

var q{S}>= 0 , integer;

var y{S,T} >= 0;

var x{S,T} >= 0;

minimize Cost: sum {i in S, j in T} x[i,j] * (a[i,j] + 10) + sum {i in S, j in T} y[i,j] * (a[i,j] + 20) + sum{i in S} f1[i] * p[i] + sum{i in S} f2[i] * q[i] ;

Capacityp {i in S}: sum {j in T} x[i,j] <= c1[i] * p[i];

Capacityq {i in S}: sum {j in T} y[i,j] <= c2[i] * q[i];

Demandp {j in T} : sum {i in S} x[i,j] >= d1[j];

Demandq {j in T} : sum {i in S} y[i,j] >= d2[j];

con1 {i in S}: p[i]<= 3;

con2 {i in S}: q[i]<= 3;

cons1: p[1]=1;

cons2: q[1]=1;

option solver cplex;





