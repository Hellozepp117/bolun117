 clear all;
 
%setpaths3
close all
 
h=fig('units','inches','width',8,'height',8,'font','Helvetica','fontsize',25)
 
 
 
 
%%
 
 
 
M=[ 0.30812281  0.14627793
  0.14627793  0.2688790 ]
 
M=[0.29306372  0.20558883
  0.20558883  0.40954738]

MX=[ 0.33989717  0.13798758
  0.13798758  0.39283177]

     xx=-100:0.00001:100;
     
        t=-3*pi:0.001:3*pi;
    xx=cos(t)';
    yy=sin(t)';
    X=[xx,yy]
    X=M*X'
    X=X'
    xx=X(:,1)
    yy=X(:,2)
   SS = max(xx)
   SS = max(SS,max(yy))
   SS = SS*1.2
    
    plot(xx,yy,'b-','LineWidt',5)
    
     
    %%
    
    
   % title(sprintf('K = %d',K))
    axis square
  %   xlim([-SS,SS])
  %   ylim([-SS,SS])
    
    
grid on
 
 
print('-depsc', '../../../icml2017/fig/syntheticWithOutliers.eps')
 