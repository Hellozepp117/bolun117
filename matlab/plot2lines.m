
plot(X, Y, 'k-o','linewidth', 2, 'markersize', 4);

ylabel('# of constraints','fontname','�꿬��', 'fontweight', 'bold', 'fontsize', 12 );

xlabel('K2', 'fontname', '�꿬��', 'fontweight', 'bold', 'fontsize',12);

set(gca,'xtick',[1,2,3,4,5,6,7,8,9,10]);

hold on

plot(X, Z, 'k--o', 'linewidth', 2, 'markersize', 4);

legend ConcurrentConstraints ActiveConstraints

box off

legend('boxoff');

set(legend, 'fontname', '�꿬��');

set(legend, 'fontweight', '�꿬��');
hold off