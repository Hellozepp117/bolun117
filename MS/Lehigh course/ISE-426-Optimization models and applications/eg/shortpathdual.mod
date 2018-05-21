#Model

set S = 1..7;

var u{S};

maximize ShortestPath: u [1] - u [7];

con1: u[1] - u[2] <=3;

con2: u[2] - u[1] <=3;

con3: u[1] - u[4] <=10;

con4: u[4] - u[1] <=10;

con5: u[1] - u[5] <=4;

con6: u[5] - u[1] <=4;

con7: u[2] - u[3] <=4;

con8: u[3] - u[2] <=4;

con9: u[2] - u[4] <=4;

con10: u[4] - u[2] <=4;

con11: u[3] - u[4] <=5;

con12: u[4] - u[3] <=5;

con13: u[3] - u[7] <=5;

con14: u[7] - u[3] <=5;

con15: u[4] - u[5] <=4;

con16: u[5] - u[4] <=4;

con17: u[4] - u[6] <=1;

con18: u[6] - u[4] <=1;

con19: u[4] - u[7] <=1;

con20: u[7] - u[4] <=1;

con21: u[5] - u[6] <=2;

con22: u[6] - u[5] <=2;

con23: u[6] - u[7] <=10;

con24: u[7] - u[6] <=10;

option solver cplex;





