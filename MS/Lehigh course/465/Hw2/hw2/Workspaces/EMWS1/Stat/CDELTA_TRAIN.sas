if ROLE in('INPUT', 'REJECTED') then do;
if upcase(NAME) in(
'AGE6574'
'AGE75'
'BLACK'
'COLLEGE'
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
else delete;
end;
