if ROLE in('INPUT', 'REJECTED') then do;
if upcase(NAME) in(
'BLACK'
'CRIME'
'FARM'
'INCOME'
'MSAFLAG'
'POP'
'POP_CHANGE'
'POP_DENSITY'
'TURNOUT'
'WHITE'
) then ROLE='INPUT';
else do;
ROLE='REJECTED';
COMMENT = "Reg: Rejected using stepwise selection";
end;
end;
