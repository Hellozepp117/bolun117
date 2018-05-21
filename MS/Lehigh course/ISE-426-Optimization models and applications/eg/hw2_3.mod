#MODEL

var x3 >=0;

var x2 >=0;

var x1 <=0;

var x4 <=0;

minimize v: x1 + 3 * x2 + x3 - x4;

con1: x1 + x2 + x3 + x4 >= 0;

con2: x1 + x2 - x3 - x4 >= -1;

