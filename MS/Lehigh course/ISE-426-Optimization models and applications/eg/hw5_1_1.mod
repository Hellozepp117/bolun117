#Model


set T = 1..35;


param x1 {T};

param x2 {T};

param y {T};

param c;

var w1;

var w2;

var beta;

var yip {T} >= 0;

var k {T};

#option solver cplex;

#Objective function

minimize cost: 0.5 * w1 * w1 + 0.5 * w2 * w2 + c * ( sum {i in T} yip [i] );

Con {i in T}: y [i] * ( w1 * x1 [i] + w2 * x2 [i] + beta ) >= 1 - yip [i];

conk {i in T}: k [i] = y[i] * ( w1 * x1 [i] + w2 * x2 [i] + beta );

