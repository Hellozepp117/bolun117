data &EM_EXPORT_TRAIN;
	set &EM_IMPORT_DATA;
	IF msa > 0 THEN msaflag = "T";
	ELSE msaflag = "F";
run;
