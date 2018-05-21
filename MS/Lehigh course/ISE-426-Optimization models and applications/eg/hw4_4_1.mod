#Model

set S = 1..11;

set T = 4..11;
 
var u{S};

variableCon { i in T }: u [i] >= 0;

Con1: u [1] + u [4] >= 0;

Con2: u [2] + u [5] >= 0;

Con3: u [3] + u [6] >= 0;

Con4: - u [1] + u [2] + u [7] >= 0;

Con5: - u [1] + u [8] >= 1;

Con6: - u [2] + u[3] + u [9] >= 0;

Con7: - u [2] + u [10] >= 1;

Con8: - u [3] + u [11] >= 1;

option solver cplex;

minimize mincut: 2 * u [4] + 4 * u [5] + 3 * u [6] + u [7] + 3 * u [8] + 1 * u [9] + 1 * u [10] + 2 * u [11];