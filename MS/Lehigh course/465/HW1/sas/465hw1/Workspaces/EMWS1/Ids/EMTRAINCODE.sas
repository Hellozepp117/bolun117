*------------------------------------------------------------*;
* Data Source Setup;
*------------------------------------------------------------*;
libname EMWS1 "F:\465\HW1\sas\465hw1\Workspaces\EMWS1";
*------------------------------------------------------------*;
* Ids: Creating DATA data;
*------------------------------------------------------------*;
data EMWS1.Ids_DATA (label="Written by SAS")
/ view=EMWS1.Ids_DATA
;
set LIBRARY.HW1;
run;
