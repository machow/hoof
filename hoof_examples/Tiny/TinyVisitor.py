# Generated from hoof_examples/Tiny/Tiny.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TinyParser import TinyParser
else:
    from TinyParser import TinyParser

# This class defines a complete generic visitor for a parse tree produced by TinyParser.

class TinyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TinyParser#prog.
    def visitProg(self, ctx:TinyParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TinyParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:TinyParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TinyParser#Integer.
    def visitInteger(self, ctx:TinyParser.IntegerContext):
        return self.visitChildren(ctx)



del TinyParser