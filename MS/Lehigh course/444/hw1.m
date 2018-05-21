clear; clc;

up=100;
low=-100;
n=100;
a=1;
b=2;
c=3;

x1=(up-low)*rand(1,n)+low;
x2=(up-low)*rand(1,n)+low;

func=@(x,y) sign(a*x+b*y+c);
yi = arrayfun(func,x1,x2);
plot(x1,x2);