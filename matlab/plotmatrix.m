
imagesc(A)          %��ͼ
colorbar
for i = 1:2
    for j = 1:2
        text(i, j, sprintf('%d',A(j,i)))
    end
end
