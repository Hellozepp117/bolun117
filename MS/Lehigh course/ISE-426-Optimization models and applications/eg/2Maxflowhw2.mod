#Model

set S = 1..10;

param xmax{S};

var x{S} >= 0;

Con1: x [1] = x [4] + x [5];

Con2: x [10] = x [3] + x [4] + x [8];
 
Con3: x [2] = x [7] + x [9] + x [8];

Con4: x [6] = x [7] + x [5];

Con5 {i in S}: x [i] <= xmax [i];

option solver cplex;

maximize Maxflow : x [6] + x [9] + x [10];




