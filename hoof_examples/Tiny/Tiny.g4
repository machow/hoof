grammar Tiny;		

prog:	(expr ';')* ;

expr:   op=OP expr               # UnaryExpr
    |   INT                      # Integer
    ;

OP      : [-+] ;
INT     : [0-9]+ ;
