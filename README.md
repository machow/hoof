# Hoof

[![Build Status](https://travis-ci.org/machow/hoof.svg?branch=master)](https://travis-ci.org/machow/hoof)

<img width="30%" align="right" src="./logo.svg">

hoof is a python library for creating abstract syntax trees (ASTs) from [antlr](https://www.antlr.org/) parsers.

Whether you are dipping your toes in the world of parsing, or a grizzled veteran, hoof will help you get started:

* Importing and running a grammar's parser, lexer, and tree visitor.
* Using a declarative syntax to quickly create ASTs.
* Progressing to tree shaping more tricky ones.
* Quick, extensible options for error handling.

I built hoof because I found myself often repeating the same code on projects, and hitting the same surprises.
Building, debugging, and shaping the output of parsers can seem daunting--hoof makes it a little easier to get started!

## Install

```
pip install hoof
```

<br>

<table>
  <tbody>
    <tr>
      <th colspan=3>Jump to Example...</td>
    </tr>
    <tr>
      <td align="center"><a href="#example-parsing-text">Parsing text</a><br>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>    
        <span>&nbsp;&nbsp;</span>
      </td>
      <td align="center"><a href="#example-create-a-simple-ast">Create a simple AST</a><br>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>        
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;</span>
      </td>
      <td align="center"><a href="#example-create-an-executable-python-ast">Create and run the python AST</a><br>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>    
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>     
        <span>&nbsp;&nbsp;</span>        
      </td>
    </tr>
  </tbody>
</table>

<br>

## Example: Parsing text

First, let's consider grammar in hoof_examples/Tiny.

```antlr4
grammar Tiny;

prog:   (body=expr ';')* ;

expr:   OP? expr                  # UnaryExpr
    |   INT                       # Integer
    ;

OP      : [-+] ;
INT     : [0-9]+ ;
```


```python
from hoof import Hoof, to_symbol

tiny_lang = Hoof("hoof_examples.Tiny")
tree1 = tiny_lang.parse("-1", "expr", mode = "parser")
tree1
```




    <hoof_examples.Tiny.TinyParser.TinyParser.UnaryExprContext at 0x1107e22b0>



Note that UnaryExprContext is a antlr4.RuleNode. These let us examine parts of the parse tree, but can be hard to investigate. A nice way to get a feel for what's going on is by using hoof's `to_symbol` function.


```python
to_symbol(tree1)
```




    █─'UnaryExprContext'
    ├─'-'
    └─█─'IntegerContext'
      └─'1'



The names next to the black boxes show us what rules were matched. The first was UnaryExpr from the first line in our grammar rule, "expr".

```
expr:   OP? expr                  # UnaryExpr
    |   INT                       # Integer
    ;
```

We can also check the full text for a node


```python
tree1.getText()
```




    '-1'



### Moving down the tree

The UnaryExpr context matches an `OP` and `expr`. We can get the matches for these two things individually.


```python
op = tree1.OP()
expr = tree1.expr()

op
```




    <antlr4.tree.Tree.TerminalNodeImpl at 0x1107e25c0>




```python
(op.getText(), expr.getText())
```




    ('-', '1')



We can also get all of its children.


```python
[child.getText() for child in tree1.children]
```




    ['-', '1']



### Rules get matched recursively


```python
tree2 = tiny_lang.parse("+-1", "expr", mode = "parser")
to_symbol(tree2)
```




    █─'UnaryExprContext'
    ├─'+'
    └─█─'UnaryExprContext'
      ├─'-'
      └─█─'IntegerContext'
        └─'1'




```python
print('outer UnaryExpr:', tree2.getText())
print('inner UnaryExpr:', tree2.expr().getText())
```

    outer UnaryExpr: +-1
    inner UnaryExpr: -1


### Multiple matches are stored in lists

Now let's look at the "prog" rule:

```
prog:   (body=expr ';')* ;
```

The `*` means that it can match the piece in the parentheses 0 or more times.


```python
tree2 = tiny_lang.parse("1;-2;", "prog", mode = "parser")
to_symbol(tree2)
```




    █─'ProgContext'
    ├─█─'IntegerContext'
    │ └─'1'
    ├─';'
    ├─█─'UnaryExprContext'
    │ ├─'-'
    │ └─█─'IntegerContext'
    │   └─'2'
    └─';'




```python
# tree2.expr() is a list
for ii, expr in enumerate(tree2.expr()):
    print("Expression", ii, "----")
    print(to_symbol(expr))
    print()
```

    Expression 0 ----
    █─'IntegerContext'
    └─'1'
    
    Expression 1 ----
    █─'UnaryExprContext'
    ├─'-'
    └─█─'IntegerContext'
      └─'2'
    


## Example: Create a simple AST

```antlr4
grammar Tiny;

prog:   (body=expr ';')* ;

expr:   OP? expr                  # UnaryExpr
    |   INT                       # Integer
    ;

SUB      : [-+] ;
INT     : [0-9]+ ;
```


```python
from hoof import Hoof, AntlrAst, to_symbol

tiny_lang = Hoof("hoof_examples.Tiny")

class UnaryOp(AntlrAst):
    _fields = ('op', 'expr')
    _remap  = ['OP->op']
    _rules  =  'UnaryExpr'

class Visitor(tiny_lang.Visitor):
    def visitTerminal(self, ctx):
        return ctx.getText()
    
tiny_lang.register(UnaryOp)
tiny_lang.bind(Visitor)

ast_tree = tiny_lang.parse("-+1", "expr")
ast_tree
```




    UnaryOp(op='-', expr=UnaryOp(op='+', expr='1'))




```python
ast_tree.op
```




    '-'



## Example: Create an executable python AST

**TODO: handle issues. (1) convert strings to ints, (2) labels on single tokens not applied**

```antlr4
grammar Tiny;

prog:   (body=expr ';')* ;

expr:   OP? expr                  # UnaryExpr
    |   INT                       # Integer
    ;

SUB      : [-+] ;
INT     : [0-9]+ ;
```


```python
from hoof import Hoof, AntlrAst, to_symbol, DispatchError
import ast

tiny_lang = Hoof("hoof_examples.Tiny")
tree1 = tiny_lang.parse("-1", "expr", mode = "parser")
to_symbol(tree1, explicit = True)
```




    █─'UnaryExprContext'
    ├─█─'TerminalNodeImpl'
    │ └─'-'
    └─█─'IntegerContext'
      └─█─'TerminalNodeImpl'
        └─'1'




```python
print("Parsed Python AST")
to_symbol(ast.parse('-1', mode = "eval"))
```

    Parsed Python AST





    █─'Expression'
    └─body = █─'UnaryOp'
             ├─op = █─'USub'
             └─operand = █─'Num'
                         └─n = 1




```python
py_ast = ast.UnaryOp(op = ast.USub(), operand = ast.Num(n = 1))

print("Manual Python AST")
to_symbol(py_ast)
```

    Manual Python AST





    █─'UnaryOp'
    ├─op = █─'USub'
    └─operand = █─'Num'
                └─n = 1




```python
from hoof import TokenDispatcher

OP_TO_AST = {
    '-': ast.USub,
    '+': ast.UAdd
}

td = TokenDispatcher(tiny_lang.Parser)
td.register("OP",  lambda ctx: OP_TO_AST[ctx.getText()]())
td.register("INT", lambda ctx: int(ctx.getText()))

class Visitor(tiny_lang.Visitor):

    def visitTerminal(self, ctx):        
        try:
            return td(ctx)
        except DispatchError:
            return ctx.getText()
        
    tiny_lang.register("UnaryExpr", ast.UnaryOp, ["OP->op", "expr->operand"])
    tiny_lang.register("Integer",   ast.Num, ["INT->n"])

# new visitor saved as tiny_lang.HoofVisitor
tiny_lang.bind(Visitor)

py_ast2 = tiny_lang.parse("-1", "expr", mode = "ast")
```


```python
ast.dump(py_ast2)
```




    'UnaryOp(op=USub(), operand=Num(n=1))'



## Common Issues

### Misnamed visitor methods

E.g. visitTerm when you meant visitTerminal

### Surprising quirks in parse tree

* Label over single token not used
* the default visitor is visitChildren, which uses defaultResult. defaultResult -> None.

## Generate parsers

```
docker run --rm -v $(pwd):/usr/src/app antlr /bin/bash -c "antlr4 -Dlanguage=Python3 -visitor tests/Expr.g4"
```
