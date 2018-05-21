#MODEL

var x3 >=0;

var x2 >=0;

var x1 >=0;

var x4 >=0;

minimize v: 3 * x1 + 2 * x2 - x3 + 25 * x4;

con1: -2 * x3 + 3 * x4 <= 0;

con2: x1 + x4 >= 1;

con3: x1 - 2 * x3 + 2 * x4 = 0;

con5: x1 + x2 - x3 + x4 >= 1;

con6: 3 * x1 - x2 - x3 - x4 = 0;

con7: x1 - x2 + 2 * x3 >= 2;

