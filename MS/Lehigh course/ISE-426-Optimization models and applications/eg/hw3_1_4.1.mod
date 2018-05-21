#MODEL

param ep = 0.0000000001;

param m1 = 1;

param m2 = 1000;

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

var z1 binary;

var z2 binary;

var z3 binary;

var z31 binary;

var z32 binary;

var z4 binary;

var z5 binary;

var z6 binary;

var z61 binary;

var z62 binary;

var z7 binary;

minimize v: z1 + z2 + z3 + z4 + z5 + z6 + z7;

con1: -2 * x3 + 3 * x4 <= 0 + y1p;

con2: x1 + x4 >= 1 - y2m;

con3: x1 - 2 * x3 + 2 * x4 = 0 + y3p - y3m;

con4: x2 + x4 <= 0 + y4p;

con5: x1 + x2 - x3 + x4 >= 1 - y5m;

con6: 3 * x1 - x2 - x3 - x4 = 0 + y6p - y6m;

con7: x1 - x2 + 2 * x3 >= 2 - y7m ;

con11: y1p >= - m1 * ( 1 - z1 ) + ep;

con12: y1p <= m2 * z1;

con41: y4p >= - m1 * ( 1 - z4 ) + ep;

con42: y4p <= m2 * z4;

con21: y2m >= - m1 * ( 1 - z2 ) + ep;

con22: y2m <= m2 * z2;

con51: y5m >= - m1 * ( 1 - z5 ) + ep;

con52: y5m <= m2 * z5;

con71: y7m >= - m1 * ( 1 - z7 ) + ep;

con72: y7m <= m2 * z7;

con31: y3p - y3m >= - m1 * ( 1 - z31 ) + ep;

con32: y3p - y3m <= m2 * z31;

con33: y3m - y3p >= - m1 * ( 1 - z32 ) + ep;

con34: y3m - y3p <= m2 * z32;

con35: z3 >= z31;

con36: z3 >= z32;

con37: z3 <= z31 + z32;

con61: y6p - y6m >= - m1 * ( 1 - z61 ) + ep;

con62: y6p - y6m <= m2 * z61;

con63: y6m - y6p >= - m1 * ( 1 - z62 ) + ep;

con64: y6m - y6p <= m2 * z62;

con65: z6 >= z61;

con66: z6 >= z62;

con67: z6 <= z61 + z62;