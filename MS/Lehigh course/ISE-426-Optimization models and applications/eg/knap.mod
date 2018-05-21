param n;
set S = 1..n;
var x {S} binary;
param C;
param w {S};
param p {S};
minimize z: sum {i in S} w[i] * x[i];
pay_ticket: sum {i in S} p[i] * x[i] >= C;

