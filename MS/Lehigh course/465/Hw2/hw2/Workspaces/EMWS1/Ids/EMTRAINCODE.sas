*------------------------------------------------------------*;
* Data Source Setup;
*------------------------------------------------------------*;
libname EMWS1 "C:\Users\box215\Desktop\Hw2\hw2\Workspaces\EMWS1";
*------------------------------------------------------------*;
* Ids: Creating DATA data;
*------------------------------------------------------------*;
data EMWS1.Ids_DATA (label="Written by SAS")
/ view=EMWS1.Ids_DATA
;
set HW2.COUNTIES;
run;
