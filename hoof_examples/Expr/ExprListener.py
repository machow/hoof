# Generated from tests/Expr.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):

    # Enter a parse tree produced by ExprParser#prog.
    def enterProg(self, ctx:ExprParser.ProgContext):
        pass

    # Exit a parse tree produced by ExprParser#prog.
    def exitProg(self, ctx:ExprParser.ProgContext):
        pass


    # Enter a parse tree produced by ExprParser#Integer.
    def enterInteger(self, ctx:ExprParser.IntegerContext):
        pass

    # Exit a parse tree produced by ExprParser#Integer.
    def exitInteger(self, ctx:ExprParser.IntegerContext):
        pass


    # Enter a parse tree produced by ExprParser#RunExpr.
    def enterRunExpr(self, ctx:ExprParser.RunExprContext):
        pass

    # Exit a parse tree produced by ExprParser#RunExpr.
    def exitRunExpr(self, ctx:ExprParser.RunExprContext):
        pass


    # Enter a parse tree produced by ExprParser#BinaryExpr.
    def enterBinaryExpr(self, ctx:ExprParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by ExprParser#BinaryExpr.
    def exitBinaryExpr(self, ctx:ExprParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by ExprParser#Parentheses.
    def enterParentheses(self, ctx:ExprParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by ExprParser#Parentheses.
    def exitParentheses(self, ctx:ExprParser.ParenthesesContext):
        pass


