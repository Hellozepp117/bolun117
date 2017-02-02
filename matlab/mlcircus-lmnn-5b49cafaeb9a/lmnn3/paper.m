 clear all;
 
%setpaths3
close all
for i=1:3
h=fig('units','inches','width',8,'height',8,'font','Helvetica','fontsize',25)
end
figure(1)
clf


data = importfile('../../../python/OurMethod/src/synthetic2.txt')

y=data(:,1)
x = data(:,2:end)

idx = (y==0)
plot(x(idx,1),x(idx,2),'bo','MarkerSize',10,'MarkerFaceColor','b')
idx = (y==1)
hold on
plot(x(idx,1),x(idx,2),'rd','MarkerSize',10,'MarkerFaceColor','r')
ylim([-1.3,1.3])
xlim([-1+min(x(:,1)), max(x(:,1))+1])
grid on
%%
figure(2)
i=1
S=[6,6,8,15]

for K = [  2 3 4 10 ]
SS=S(i)
    maxiter=200;
    yTr = y
    xTr = x'

    % train full muodel
    fprintf('Training final model...\n');
    [L,Details] = lmnnCG(xTr, yTr,K,'maxiter',maxiter);

    M=L*L'
    
    subplot(2,2,i)
    k=10000;
    t=([1:k])/k*2*pi;
    xx=cos(t)'
    yy=sin(t)'
    X=[xx,yy]
    X=L*X'
    X=X'
    xx=X(:,1)
    yy=X(:,2)
    
     xx=-80:0.001:80;
    yy =( -2*M(1,2)*xx + ( 4*M(1,2)^2*xx.*xx    - 4 *M(2,2)*(M(1,1)*xx.*xx  -1 )        ).^0.5                )/(2*M(2,2));
    idx = (imag(yy)==0)
    hold off
    plot(xx(idx),yy(idx),'b--')
      hold on
    yy =( -2*M(1,2)*xx - ( 4*M(1,2)^2*xx.*xx    - 4 *M(2,2)*(M(1,1)*xx.*xx  -1 )        ).^0.5                )/(2*M(2,2));
    
    
    plot(xx(idx),yy(idx),'b--')
    
    title(sprintf('K = %d',K))
    axis square
     xlim([-SS,SS])
     ylim([-SS,SS])
    i=i+1
    
grid on
end   
    
figure(1)
print('-depsc', '../../../icml2017/fig/synthetic1.eps')
figure(2)
print('-depsc', '../../../icml2017/fig/synthetic1lmnn.eps')

    
    i=i+1
 