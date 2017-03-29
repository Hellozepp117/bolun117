 clear all;
 
%setpaths3
close all
 

fileName = '../../../python/OurMethod/src/datasets/diabetes_scale.txt_mTraing'
fileName = '../../../python/OurMethod/src/datasets/iris.scale.txt_mTraing'
data = importfile(fileName)

y=data(:,1)
x = data(:,2:end)

 
%%
 
 for K=[1,3, 5, 7, 11]
     
 maxiter=500;
 yTr = y
 xTr = x'

    % train full muodel
 fprintf('Training final model...\n');
 [L,Details] = lmnnCG(xTr, yTr,K,'maxiter',maxiter);

 M=L'*L;
 
fileID = fopen(sprintf('%s_matlab_%d',fileName,K),'w');
[m,n]=size(M)
for r =1:m
    for c=1:n
        
        fprintf(fileID,'%1.16f ',M(r,c));
    end
    fprintf(fileID,'\n',M);
end
fclose(fileID);
 
 end
  