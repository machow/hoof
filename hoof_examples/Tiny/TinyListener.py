# Generated from hoof_examples/Tiny/Tiny.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TinyParser import TinyParser
else:
    from TinyParser import TinyParser

# This class defines a complete listener for a parse tree produced by TinyParser.
class TinyListener(ParseTreeListener):

    # Enter a parse tree produced by TinyParser#prog.
    def enterProg(self, ctx:TinyParser.ProgContext):
        pass

    # Exit a parse tree produced by TinyParser#prog.
    def exitProg(self, ctx:TinyParser.ProgContext):
        pass


    # Enter a parse tree produced by TinyParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:TinyParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by TinyParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:TinyParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by TinyParser#Integer.
    def enterInteger(self, ctx:TinyParser.IntegerContext):
        pass

    # Exit a parse tree produced by TinyParser#Integer.
    def exitInteger(self, ctx:TinyParser.IntegerContext):
        pass


