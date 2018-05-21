#MODEL

var x >= 0;

var y1 >= 0;

var y2 >= 0;

var y3 >= 0;

var z >= 0;

maximize v: z;

con1: z <= 250 * 450 - 120 * x - 550 * y1;

con2: z <= 250 * 900 - 120 * x - 550 * y2;

con3: z <= 250 * 1250 - 120 * x - 550 * y3;

con4: x + y3 >= 1250;

con5: x + y2 >= 900;

con6: x + y1 >= 450;
