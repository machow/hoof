__version__ = "0.0.1"

import antlr4
import importlib
import itertools

# note: importing because Token module gets overshadowed
from antlr4.Token import CommonToken
from ast import AST
from functools import singledispatch

# Simple running of an antlr parser -------------------------------------------

def parse(grammar, text, start_rule, err_listener = None, err_handler = None):
    """
    Args:
        grammar: a grammar with attributes Parser, and Lexer.
        text: text to parse.
        start_rule: antlr rule to start parsing from.
        err_listener: if set to "throw" will cause parse errors to raise hoof.ParseException.
        err_handler: a custom error handler instance to set.

    """
    # https://github.com/antlr/antlr4/blob/master/doc/python-target.md
    input_stream = antlr4.InputStream(text)

    lexer = grammar.Lexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = grammar.Parser(token_stream)

    # handle error strategy ----
    if err_handler is not None:
        # this is an error handler in the sense of, if fast parsing fails, 
        # should we restart with slow parsing. Can't raise an overall error.
        parser._errHandler = err_handler

    # handle error listener ----
    err_listener = _get_listener(err_listener)

    if err_listener is not None:
        print(err_listener)
        lexer.removeErrorListeners()
        lexer.addErrorListener(err_listener)

        parser.removeErrorListeners()
        parser.addErrorListener(err_listener)

    return getattr(parser, start_rule)()

@singledispatch
def to_symbol(x):
    raise TypeError("unsupported type: %s" %type(x))

@to_symbol.register(antlr4.RuleContext)
def _to_symbol_parser(x, explicit = False):
    #from .ast import AntrlAst, dump_context, SimplifyVisitor
    from siuba import siu
    return siu.Symbolic(simplify_context(x, explicit))


def simplify_context(node, explicit = False):
    from siuba import siu
    if isinstance(node, antlr4.TerminalNode):
        if not explicit:
            return node.getText()
        
        return siu.Call(node.__class__.__name__, node.getText())

    return siu.Call(
            node.__class__.__name__,
            *map(lambda x: simplify_context(x, explicit = explicit), node.children)
            )

@to_symbol.register(AST)
def _to_symbol_ast(x):
    from siuba.siu import Symbolic
    return Symbolic(_callify(x))


def _callify(node):
    from siuba.siu import Call
    from ast import iter_fields
    if isinstance(node, (list, tuple)):
        return Call("List", *[_callify(x) for x in node])
    elif not isinstance(node, AST):
        return node

    node_name = node.__class__.__name__
    call = Call(node_name, **{field: _callify(val) for field, val in iter_fields(node)})

    return call

def _get_listener(name):
    # this is hacky, but also these options are purely a tool of convenience
    return {
            "throw": ThrowingErrorListener,
            "diagnostic": antlr4.DiagnosticErrorListener,
            None: None
    }[name]


# Hoof class: -----------------------------------------------------------------

class Hoof:
    """Load an antlr grammar, configure a visitor to create abstract syntax trees (ASTs).

    Args:
        mod_name: name of module where antlr grammar lives.
        prefix: (optional) name that is prefixed to grammar's classes.
    
    This class has three main jobs:

      * make it easier to import a grammar's parser, lexer, and visitor classes
      * create visitor methods for simple AST node construction
      * bind visitor methods to a class

    """
    def __init__(self, mod_name, prefix = None):
        self.Parser  = self._import(mod_name, "Parser", prefix)
        self.Lexer   = self._import(mod_name, "Lexer", prefix)
        self.Visitor = self._import(mod_name, "Visitor", prefix)
        self.registry = {}

        self.token_dispatcher = TokenDispatcher(self.Parser)

        self.HoofVisitor = None


    def parse(self, text, start_rule, *args, mode="ast", **kwargs):
        parse_tree = parse(self, text, start_rule, *args, **kwargs)
        if mode == "ast":
            if self.HoofVisitor is None:
                raise ValueError("must call .bind() to set HoofVisitor")
            return self.HoofVisitor().visit(parse_tree)
        elif mode == "parser":
            return parse_tree

        raise ValueError("Mode must be one of 'ast' or 'parser'")


    def register(self, ctx_name, ast_kls = None, remap = None):
        # shortcut for two alternative modes: passing on an AST node, or a token visitors
        if not isinstance(ctx_name, str) and issubclass(ctx_name, AntlrAst):
            # received AST node as first arg
            ast_kls = ctx_name
            ctx_name, remap = ast_kls._rules, ast_kls._remap
            return self.register(ctx_name, ast_kls, remap)
        elif isinstance(ctx_name, str) and ctx_name.isupper():
            # token visitor
            return self.token_dispatcher.register(ctx_name, ast_kls)

        self.registry[ctx_name] = self.create_visitor_method(ast_kls, remap)

    def dispatch(self, ctx_name):
        """Return visit method for ctx_name"""
        return self.registry[ctx_name]

    def bind(self, Visitor = None):
        if Visitor is None: Visitor = self.Visitor

        # create visit methods from registry
        new_visitors = {}
        for ctx_name, method in self.registry.items():
            method_name = "visit" + ctx_name
            new_visitors[method_name] = method

        # create new visitor class, set as HoofVisitor
        visitor_cls = type("HoofVisitor", (Visitor,), new_visitors)
        self.HoofVisitor = visitor_cls


    @staticmethod
    def _import(mod_name, kls_name, prefix = None):
        if prefix is None:
            # when no prefix, assume module name is used as prefix
            # e.g. from R.RParser import RParser
            #      from some_package.parsers.R.RParser import RParser
            prefix = mod_name.split(".")[-1]
        attr_name = prefix + kls_name
        mod = importlib.import_module("." + attr_name, mod_name)
        return getattr(mod, attr_name)


    @staticmethod
    def create_visitor_method(node_cls, spec):
        mappings = parse_spec(spec)

        # could use functools.partialmethod, but this is easier to inspect in console
        def visit_method(visitor, ctx):
            return create_node(visitor, ctx, node_cls, mappings)

        return visit_method


class DispatchError(Exception): pass

class TokenDispatcher:
    def __init__(self, Parser):
        self.registry = {}
        self._Parser = Parser
        self._token_types = {}

    def __call__(self, ctx):
        return self.dispatch(ctx)(ctx)

    def register(self, tok_name, func):
        tok_type = getattr(self._Parser, tok_name)
        self._token_types[tok_type] = tok_name
        self.registry[tok_name] = func

    def dispatch(self, ctx, default = None):
        tok_type = ctx.symbol.type
        tok_name = self._token_types.get(tok_type)

        if tok_name is not None:
            return self.registry.get(tok_name)

        raise DispatchError("no entry to dispatch for context type: %s" %tok_type)





# Tree Visiting functions -----------------------------------------------------

def parse_spec(spec = None):
    if spec is None:
        return {}

    return dict(list(entry.split("->") for entry in spec))

        
def create_node(visitor, ctx, cls, mappings = None):
    """default visiting behavior, which uses fields"""

    mappings = {} if mappings is None else mappings
    all_fields = itertools.chain(mappings.items(), zip(cls._fields, cls._fields))
        
    field_args = {}
    for src_key, dst_key in all_fields:
        if dst_key in field_args:
            continue

        child = getattr(ctx, src_key, getattr(ctx, dst_key, None))

        # when not alias needs to be called
        if not isinstance(child, antlr4.RuleNode) and callable(child):
            # Note: every time antlr4 gets a token or context through a method
            # like mycontext.expr(), it does a full loop over the children.
            # We could probably improve by looping once and identifying the
            # nodes we get here, but it would involve a lot of wrangling.
            child = child()
        elif isinstance(child, CommonToken):
            # normally you get a terminal node, but rule el labels are tokens
            # for some reason. Find which TerminalNode.symbol it came from, but
            # be mindful that context nodes don't have a symbol attr.
            child = next(
                c for c in ctx.children if getattr(c, "symbol", None) is child
            )

        if isinstance(child, (tuple, list)):
            out = [visitor.visit(el) for el in child]
        elif child:
            out = visitor.visit(child)
        else:
            out = child
        
        field_args[dst_key] = out
    return cls(_ctx = ctx, **field_args)


# AST Nodes -------------------------------------------------------------------

class AntlrAst(AST):
    """AST node holding parser context. Compatible with python AST interface."""

    # TODO: what exactly is AST._attributes? It is used in ast.dump.
    _fields = tuple()

    def __init__(self, *args, _ctx=None, **kwargs):
        # AST takes 0 or len(self._field) pos args, and any kwargs.
        # intriguingly, no validation (likely for speed?)
        #   * ast.UnaryOp(1,2).op is 1
        #   * ast.UnaryOp(1,2, op = 9).op is 9
        super().__init__(*args, **kwargs)
        self._ctx = _ctx

    def _get_text(self):
        return self._ctx.getText()

    @property
    def lineno(self):
        return self._ctx.start.line

    @property
    def col_offset(self):
        return self.ctx.start.column

    @property
    def end_lineno(self):
        return self.ctx.stop.line

    @property
    def end_col_offset(self):
        # TODO: what happens with UTF-8 characters? If it is the 10th character
        #       to the human eye, but that is char + combining char, is this 11?
        #       eg does it count the combining character as +1
        # position of last token + its width
        return self.stop.column + ctx.stop.stop - ctx.stop.start

    def __repr__(self):
        import ast
        return ast.dump(self)


def dump_dict(node):
    """Dump a node as a dict.

    Note that this follows the same behavior as python AST nodes. Namely, if a
    field has no child set on the node, it is *not* set to None, but doesn't exist.

    Eg ast.BinOp() does not have an op attribute.
    """
    if isinstance(node, (list, tuple)):
        return [dump_dict(x) for x in node]

    if isinstance(node, AntlrAst):
        children = {}
        for name in node._fields:
            raw = getattr(node, name, None)

            if raw is None:
                continue
            
            if isinstance(raw, AntlrAst):
                child = dump_dict(raw)
            elif isinstance(raw, list):
                child = [dump_dict(x) for x in raw]
            else:
                child = raw

            children[name] = child
        return {
                "type": node.__class__.__name__,
                "children": children,
                "fields": node._fields
                }

    return node

def dump_context(node):
    """Return a parse tree as a simple dictionary."""
    start = getattr(node, 'start', None) or node.symbol
    stop  = getattr(node, 'stop', None) or node.symbol

    children = getattr(node, 'children', tuple())
    return dict(
            name = node.__class__.__name__.replace("Context", ""),
            text = node.getText(),
            line_info = {
                "col_start": start.start,
                "line_start": start.line,
                "col_end": stop.stop,
                "line_end": stop.line,
                },
            children = tuple(map(dump_context, children))
            )


# Error Listeners -------------------------------------------------------------

from antlr4.error.ErrorListener import ErrorListener

class ParsingException(Exception):
    pass


class ThrowingErrorListener(ErrorListener):
    # converts this JAVA approach: https://stackoverflow.com/a/26573239/1144523
    # error message is from the antlr4.error.ConsoleErrorListener
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = "line {line}:{column} {msg}".format(
                        line=line, column=column, msg=msg
                        )
        raise ParsingException(error_msg) from e 

