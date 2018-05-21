#Model

set Months = 1..12;


set MonthsPlus = 0..12;


param cost {Months};


param ProdCap;


param InvCap;


param demand {Months};


var production {Months} >= 0 <= ProdCap;


var inventory {MonthsPlus} >= 0 <= InvCap;


option solver cplex;


#Objective 
minimize prodCost: sum {i in Months} cost [i] * production [i];


conservation {i in Months}: production [i] + inventory [i-1] = demand [i] + inventory [i];


Jan1Inv: inventory [0] = 0;


Dec31Inv: inventory [12] = 0;