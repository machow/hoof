# Generated from hoof_examples/Tiny/Tiny.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\5")
        buf.write("\22\b\1\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\3\3\3\3\4\6")
        buf.write("\4\17\n\4\r\4\16\4\20\2\2\5\3\3\5\4\7\5\3\2\4\4\2--//")
        buf.write("\3\2\62;\2\22\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\3\t")
        buf.write("\3\2\2\2\5\13\3\2\2\2\7\16\3\2\2\2\t\n\7=\2\2\n\4\3\2")
        buf.write("\2\2\13\f\t\2\2\2\f\6\3\2\2\2\r\17\t\3\2\2\16\r\3\2\2")
        buf.write("\2\17\20\3\2\2\2\20\16\3\2\2\2\20\21\3\2\2\2\21\b\3\2")
        buf.write("\2\2\4\2\20\2")
        return buf.getvalue()


class TinyLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    OP = 2
    INT = 3

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'" ]

    symbolicNames = [ "<INVALID>",
            "OP", "INT" ]

    ruleNames = [ "T__0", "OP", "INT" ]

    grammarFileName = "Tiny.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


