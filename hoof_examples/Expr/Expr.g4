grammar Expr;		

prog:	(expr ';')* ;

expr:   left=expr op=('+'|'-') right=expr      # BinaryExpr
    |   RUN expr                               # RunExpr
    |	INT                                    # Integer
    |	'(' expr ')'                           # Parentheses
    ;

RUN     : 'run' ;
INT     : [0-9]+ ;

WS  :   [ \t\u000C]+ -> skip ;
