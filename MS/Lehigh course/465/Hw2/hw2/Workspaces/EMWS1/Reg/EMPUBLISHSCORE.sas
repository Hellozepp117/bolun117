*************************************;
*** begin scoring code for regression;
*************************************;

length _WARN_ $4;
label _WARN_ = 'Warnings' ;


drop _DM_BAD;
_DM_BAD=0;

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

*** Check white for missing values ;
if missing( white ) then do;
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
   goto REGDR1;
end;

*** Compute Linear Predictor;
drop _TEMP;
drop _LP0;
_LP0 = 0;

***  Effect: black ;
_TEMP = black ;
_LP0 = _LP0 + (    0.12150170661219 * _TEMP);

***  Effect: crime ;
_TEMP = crime ;
_LP0 = _LP0 + (   -0.00037276104077 * _TEMP);

***  Effect: farm ;
_TEMP = farm ;
_LP0 = _LP0 + (   -0.45883380841637 * _TEMP);

***  Effect: income ;
_TEMP = income ;
_LP0 = _LP0 + (   -0.00040506908567 * _TEMP);

***  Effect: msaflag ;
_TEMP = 1;
_LP0 = _LP0 + (    -0.6391589161978) * _TEMP * _0_0;

***  Effect: pop ;
_TEMP = pop ;
_LP0 = _LP0 + (  5.0223756974192E-6 * _TEMP);

***  Effect: pop_change ;
_TEMP = pop_change ;
_LP0 = _LP0 + (   -0.07983763839065 * _TEMP);

***  Effect: pop_density ;
_TEMP = pop_density ;
_LP0 = _LP0 + (    0.00072026318409 * _TEMP);

***  Effect: turnout ;
_TEMP = turnout ;
_LP0 = _LP0 + (    0.05996192806021 * _TEMP);

***  Effect: white ;
_TEMP = white ;
_LP0 = _LP0 + (   -0.13829422201736 * _TEMP);
*--- Intercept ---*;
_LP0 = _LP0 + (    63.8831324948399);

REGDR1:

*** Predicted Value;
label P_democrat = 'Predicted: democrat' ;
P_democrat = _LP0;


*************************************;
***** end scoring code for regression;
*************************************;
