# Generated from tests/Expr.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#prog.
    def visitProg(self, ctx:ExprParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Integer.
    def visitInteger(self, ctx:ExprParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#RunExpr.
    def visitRunExpr(self, ctx:ExprParser.RunExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:ExprParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Parentheses.
    def visitParentheses(self, ctx:ExprParser.ParenthesesContext):
        return self.visitChildren(ctx)



del ExprParser