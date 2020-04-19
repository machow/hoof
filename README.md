# Hoof

<img width="30%" align="right" src="./logo.svg">

hoof is a python library for creating abstract syntax trees (ASTs) from [antlr](https://www.antlr.org/) parsers.

Whether you are dipping your toes in the world of parsing, or a grizzled veteran, hoof will help you get started:

* Importing and running a grammar's parser, lexer, and tree visitor.
* Using a declarative syntax to quickly create ASTs.
* Progressing to tree shaping more tricky ones.
* Quick, extensible options for error handling.

I built hoof because I found myself often repeating the same code, and hitting the
same surprises when working on projects. Building, debugging, and shaping the output of
parsers can seem daunting--hopefully hoof makes it a little easier to get started!

## Install


## Examples


## Generate parsers

```
docker run --rm -v $(pwd):/usr/src/app antlr /bin/bash -c "antlr4 -Dlanguage=Python3 -visitor tests/Expr.g4"
```

## References

* [antlr website](https://www.antlr.org/)
* Logo was (very mildly) adapted from this image from [paintingvalley](https://paintingvalley.com/moose-drawing-outline#moose-drawing-outline-2.jpg) (claimed CC BY-NC 4.0). If you want to contribute one with less dubious origins, let me know!
