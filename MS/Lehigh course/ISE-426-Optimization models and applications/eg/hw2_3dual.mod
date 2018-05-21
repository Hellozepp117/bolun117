#MODEL

var u1 >=0;

var u2 >=0;

maximize v: -u2;

con1: u1+u2 >= 1;

con2: u1+u2 <= 3;

con3: u1-u2 <= 1;

con4: u1-u2 >= -1;

