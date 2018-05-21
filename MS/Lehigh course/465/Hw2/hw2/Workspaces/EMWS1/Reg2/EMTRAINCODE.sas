*------------------------------------------------------------*;
* Reg2: Create decision matrix;
*------------------------------------------------------------*;
data WORK.democrat(label="democrat");
  length   democrat                             8
           ;

 democrat=6.8000001907;
output;
 democrat=84.599998474;
output;
 democrat=45.69999933235;
output;
;
run;
proc datasets lib=work nolist;
modify democrat(type=PROFIT label=democrat);
run;
quit;
data EM_DMREG / view=EM_DMREG;
set EMWS1.Drop2_TRAIN(keep=
age6574 black crime democrat farm income msaflag pop pop_change pop_density
turnout);
run;
*------------------------------------------------------------* ;
* Reg2: DMDBClass Macro ;
*------------------------------------------------------------* ;
%macro DMDBClass;
    msaflag(ASC)
%mend DMDBClass;
*------------------------------------------------------------* ;
* Reg2: DMDBVar Macro ;
*------------------------------------------------------------* ;
%macro DMDBVar;
    age6574 black crime democrat farm income pop pop_change pop_density turnout
%mend DMDBVar;
*------------------------------------------------------------*;
* Reg2: Create DMDB;
*------------------------------------------------------------*;
proc dmdb batch data=WORK.EM_DMREG
dmdbcat=WORK.Reg2_DMDB
maxlevel = 513
;
class %DMDBClass;
var %DMDBVar;
target
democrat
;
run;
quit;
*------------------------------------------------------------*;
* Reg2: Run DMREG procedure;
*------------------------------------------------------------*;
proc dmreg data=EM_DMREG dmdbcat=WORK.Reg2_DMDB
validata = EMWS1.Drop2_VALIDATE
outest = EMWS1.Reg2_EMESTIMATE
outterms = EMWS1.Reg2_OUTTERMS
outmap= EMWS1.Reg2_MAPDS namelen=200
;
class
msaflag
;
model democrat =
age6574
black
crime
farm
income
msaflag
pop
pop_change
pop_density
turnout
/error=normal
coding=DEVIATION
nodesignprint
;
;
code file="C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Reg2\EMPUBLISHSCORE.sas"
group=Reg2
;
code file="C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Reg2\EMFLOWSCORE.sas"
group=Reg2
residual
;
run;
quit;
