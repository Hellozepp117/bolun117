*************************************;
*** begin scoring code for regression;
*************************************;

length _WARN_ $4;
label _WARN_ = 'Warnings' ;

drop _Y;
_Y = democrat ;

drop _DM_BAD;
_DM_BAD=0;

*** Check age6574 for missing values ;
if missing( age6574 ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check black for missing values ;
if missing( black ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check crime for missing values ;
if missing( crime ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check farm for missing values ;
if missing( farm ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check income for missing values ;
if missing( income ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check pop for missing values ;
if missing( pop ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check pop_change for missing values ;
if missing( pop_change ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check pop_density for missing values ;
if missing( pop_density ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check turnout for missing values ;
if missing( turnout ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Generate dummy variables for msaflag ;
drop _0_0 ;
if missing( msaflag ) then do;
   _0_0 = .;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;
else do;
   length _dm1 $ 1; drop _dm1 ;
   %DMNORMCP( msaflag , _dm1 )
   if _dm1 = 'F'  then do;
      _0_0 = 1;
   end;
   else if _dm1 = 'T'  then do;
      _0_0 = -1;
   end;
   else do;
      _0_0 = .;
      substr(_warn_,2,1) = 'U';
      _DM_BAD = 1;
   end;
end;

*** If missing inputs, use averages;
if _DM_BAD > 0 then do;
   _LP0 =     39.6370183454741;
   goto REG2DR1;
end;

*** Compute Linear Predictor;
drop _TEMP;
drop _LP0;
_LP0 = 0;

***  Effect: age6574 ;
_TEMP = age6574 ;
_LP0 = _LP0 + (     0.0198593515468 * _TEMP);

***  Effect: black ;
_TEMP = black ;
_LP0 = _LP0 + (      0.237290436576 * _TEMP);

***  Effect: crime ;
_TEMP = crime ;
_LP0 = _LP0 + (   -0.00031371068777 * _TEMP);

***  Effect: farm ;
_TEMP = farm ;
_LP0 = _LP0 + (    -0.4547872370288 * _TEMP);

***  Effect: income ;
_TEMP = income ;
_LP0 = _LP0 + (   -0.00042794810158 * _TEMP);

***  Effect: msaflag ;
_TEMP = 1;
_LP0 = _LP0 + (    -0.5606903029766) * _TEMP * _0_0;

***  Effect: pop ;
_TEMP = pop ;
_LP0 = _LP0 + (  5.7436379416193E-6 * _TEMP);

***  Effect: pop_change ;
_TEMP = pop_change ;
_LP0 = _LP0 + (   -0.07416135567369 * _TEMP);

***  Effect: pop_density ;
_TEMP = pop_density ;
_LP0 = _LP0 + (    0.00076350366853 * _TEMP);

***  Effect: turnout ;
_TEMP = turnout ;
_LP0 = _LP0 + (    0.01355519899657 * _TEMP);
*--- Intercept ---*;
_LP0 = _LP0 + (    52.9670771529046);

REG2DR1:

*** Predicted Value, Error, and Residual;
label P_democrat = 'Predicted: democrat' ;
P_democrat = _LP0;

drop _R;
if _Y = . then do;
   R_democrat = .;
end;
else do;
   _R = _Y - _LP0;
    label R_democrat = 'Residual: democrat' ;
   R_democrat = _R;
end;

*************************************;
***** end scoring code for regression;
*************************************;
