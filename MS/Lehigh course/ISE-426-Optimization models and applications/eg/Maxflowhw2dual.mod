#Model

set S = 1..14;

set T = 5..14;
 
var u{S};

variableCon { i in T }: u [i] >= 0;

Con1: u [1] + u [5] >= 1;

Con2: u [3] + u [6] >= 1;

Con3: u [2] + u [7] >= 1;

Con4: - u [1] + u [2] + u [8] >= 0;

Con5: - u [1] + u [4] + u [9] >= 0;

Con6: - u [4] + u [10] >= 0;

Con7: - u [3] + u [4] + u [11] >= 0;

Con8: - u [3] + u [2] + u [12] >= 0;

Con9: - u [3] + u [13] >= 0;

Con10: - u [2] + u [14] >= 0;

option solver cplex;

minimize mincut: 5 * u [5] + 4 * u [6] + 3 * u [7] + u [8] + 3 * u [9] + 5 * u [10] + 3 * u [11] + 3 * u [12] + 3 * u [13] + 8 * u [14];