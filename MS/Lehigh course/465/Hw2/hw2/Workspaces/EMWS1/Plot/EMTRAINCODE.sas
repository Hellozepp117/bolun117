*------------------------------------------------------------* ;
* Plot: DMDBClass Macro ;
*------------------------------------------------------------* ;
%macro DMDBClass;
    age6574(ASC) age75(ASC) black(ASC) college(ASC) crime(ASC) democrat(DESC)
   farm(ASC) income(ASC) msaflag(ASC) pop(ASC) pop_change(ASC) pop_density(ASC)
   turnout(ASC) white(ASC)
%mend DMDBClass;
*------------------------------------------------------------*;
* Plot: Create DMDB;
*------------------------------------------------------------*;
proc dmdb batch data=EMWS1.Part_TRAIN
dmdbcat=WORK.Plot_DMDB
maxlevel = 23
nonorm
;
class %DMDBClass;
target
democrat
;
run;
quit;
*------------------------------------------------------------*;
* Plot: Creating univariate histograms;
*------------------------------------------------------------*;
goptions ftext="SWISS";
goptions nodisplay device=PNG;
axis1 width=2 offset=(1,1) label=(rotate=90 angle=270) minor=none;
axis2 width=2 minor=none;
pattern1 value=solid;
proc gchart
data=EMWS1.Part_TRAIN gout=WORK.PlotGRAPH;
*;
title "age6574";
vbar age6574 /
name = "age6574" description = "age6574"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "age75";
vbar age75 /
name = "age75" description = "age75"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "black";
vbar black /
name = "black" description = "black"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "college";
vbar college /
name = "college" description = "college"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "crime";
vbar crime /
name = "crime" description = "crime"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "democrat";
vbar democrat /
name = "democrat" description = "democrat"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "farm";
vbar farm /
name = "farm" description = "farm"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "income";
vbar income /
name = "income" description = "income"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "msaflag";
vbar msaflag /
name = "msaflag" description = "msaflag"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop";
vbar pop /
name = "pop" description = "pop"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop_change";
vbar pop_change /
name = "pop_change" description = "pop_change"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop_density";
vbar pop_density /
name = "pop_density" description = "pop_density"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "turnout";
vbar turnout /
name = "turnout" description = "turnout"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "white";
vbar white /
name = "white" description = "white"
FREQ
type=FREQ
noframe
missing
raxis=axis1 maxis=axis2;
run;
quit;
title;
goptions display;
*------------------------------------------------------------*;
* Plot: Creating variable by interval target charts;
*------------------------------------------------------------*;
goptions ftext="SWISS";
goptions nodisplay device=PNG;
axis1 width=2 offset=(1,1) label=(rotate=90 angle=270) minor=none;
axis2 width=2 minor=none;
pattern1 value=solid;
proc gchart
data=EMWS1.Part_TRAIN gout=WORK.PlotGRAPH;
*;
title "age6574 vs democrat (mean)";
vbar age6574 /
name = "age6574        x democrat       " description = "age6574 vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "age75 vs democrat (mean)";
vbar age75 /
name = "age75          x democrat       " description = "age75 vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "black vs democrat (mean)";
vbar black /
name = "black          x democrat       " description = "black vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "college vs democrat (mean)";
vbar college /
name = "college        x democrat       " description = "college vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "crime vs democrat (mean)";
vbar crime /
name = "crime          x democrat       " description = "crime vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "farm vs democrat (mean)";
vbar farm /
name = "farm           x democrat       " description = "farm vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "income vs democrat (mean)";
vbar income /
name = "income         x democrat       " description = "income vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "msaflag vs democrat (mean)";
vbar msaflag /
name = "msaflag        x democrat       " description = "msaflag vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop vs democrat (mean)";
vbar pop /
name = "pop            x democrat       " description = "pop vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop_change vs democrat (mean)";
vbar pop_change /
name = "pop_change     x democrat       " description = "pop_change vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "pop_density vs democrat (mean)";
vbar pop_density /
name = "pop_density    x democrat       " description = "pop_density vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "turnout vs democrat (mean)";
vbar turnout /
name = "turnout        x democrat       " description = "turnout vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
title "white vs democrat (mean)";
vbar white /
name = "white          x democrat       " description = "white vs democrat (mean)"
MEAN
type=MEAN
sumvar=democrat MEAN
noframe
missing
raxis=axis1 maxis=axis2;
run;
quit;
title;
goptions display;
*------------------------------------------------------------*;
* Plot: Copying graphs to node folder;
*------------------------------------------------------------*;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\age6574.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay AGE6574;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\age6574 vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay AGE65741;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\age75.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay AGE75;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\age75 vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay AGE751;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\black.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay BLACK;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\black vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay BLACK1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\college.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay COLLEGE;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\college vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay COLLEGE1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\crime.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay CRIME;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\crime vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay CRIME1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\democrat.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay DEMOCRAT;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\farm.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay FARM;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\farm vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay FARM1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\income.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay INCOME;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\income vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay INCOME1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\msaflag.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay MSAFLAG;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\msaflag vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay MSAFLAG1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop_change vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP_CHA1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop_change.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP_CHAN;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop_density vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP_DEN1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\pop_density.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay POP_DENS;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\turnout.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay TURNOUT;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\turnout vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay TURNOUT1;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\white.gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay WHITE;
quit;
goptions device=win;
filename gsasfile;
filename gsasfile "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1\Plot\GRAPH\white vs democrat (mean).gif";
goptions device= ZGIF display gaccess= gsasfile gsfmode= replace cback= white;
proc greplay igout=WORK.PLOTGRAPH nofs;
replay WHITE1;
quit;
goptions device=win;
filename gsasfile;
