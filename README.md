# Hoof

<img width="30%" align="right" src="./logo.svg">

hoof is a python library for creating abstract syntax trees (ASTs) from [antlr](https://www.antlr.org/) parsers.

Whether you are dipping your toes in the world of parsing, or a grizzled veteran, hoof will help with...

* Importing and running a grammar's parser, lexer, and tree visitor.
* Using a declarative syntax to quickly create ASTs.
* Progressing to tree shaping more tricky ones.
* Quick, extensible options for error handling.

## Install


## Examples


## Generate parsers

```
docker run --rm -v $(pwd):/usr/src/app antlr /bin/bash -c "antlr4 -Dlanguage=Python3 -visitor tests/Expr.g4"
```
