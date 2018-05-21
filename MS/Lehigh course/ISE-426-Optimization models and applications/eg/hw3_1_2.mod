#MODEL

var x3 >=0;

var x2 >=0;

var x1 >=0;

var x4 >=0;

var y1p >=0;

var y2m >=0;

var y3m >=0;

var y3p >=0;

var y4p >=0;

var y5m >=0;

var y6p >=0;

var y6m >=0;

var y7m >=0;

minimize v: y1p + y2m + y3m + y3p + y4p + y5m + y6p + y6m + y7m;

con1: -2 * x3 + 3 * x4 <= 0 + y1p;

con2: x1 + x4 >= 1 - y2m;

con3: x1 - 2 * x3 + 2 * x4 = 0 + y3p - y3m;

con4: x2 + x4 <= 0 + y4p;

con5: x1 + x2 - x3 + x4 >= 1 - y5m;

con6: 3 * x1 - x2 - x3 - x4 = 0 + y6p - y6m;

con7: x1 - x2 + 2 * x3 >= 2 -y7m ;

