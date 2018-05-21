clear; clc;

x1 = -3:0.05:3;
x2 = -3:0.05:3;
[x1,x2] = meshgrid(x1,x2);

func = @(x,y) 2*x^2 + 1*y^2 + 1*x*y + 1*x + 1*y - 3;

z = arrayfun(func,x1,x2);

figure(); hold on;
contour(x1,x2,z,[0 0],'b-');
contour(x1,x2,z,[-1 1],'y:');
contour(x1,x2,z,[2 2],'b-');