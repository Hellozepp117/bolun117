 clear all;
 
%setpaths3
close all
for i=1:1
h=fig('units','inches','width',12,'height',12,'font','Helvetica','fontsize',22)
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
 axis square
xlim([-1+min(x(:,1)), max(x(:,1))+1])
ylim([-30, 30])
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
    
    subplot(1,4,i)
    
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
    hold off
    plot(xx ,yy ,'b-','LineWidth',7)
     
    title(sprintf('K = %d',K))
    axis square
     xlim([-SS,SS])
     ylim([-SS,SS])
    i=i+1
    
grid on
end   
    %%
figure(1)
legend('Class 1','Class 2')
print('-depsc', '../../../icml2017/fig/synthetic1.eps')


%%
figure(2)
print('-depsc', '../../../icml2017/fig/synthetic1lmnn.eps')

    
    i=i+1
 