# Hoof

## Generating parsers

```
docker run --rm -v $(pwd):/usr/src/app antlr /bin/bash -c "antlr4 -Dlanguage=Python3 -visitor tests/Expr.g4"
```
