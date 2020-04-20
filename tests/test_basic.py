from hoof import Hoof, AntlrAst

class Program(AntlrAst):
    _fields = ["body"]

class BinaryExpr(AntlrAst):
    _fields = ["left", "right", "op"]

class RunExpr(AntlrAst):
    _fields = ["op", "expr"]
    _remap  = ["RUN->op"]
    _rules  = "RunExpr"


hoof = Hoof("hoof_examples.Expr")

class AstVisitor(hoof.Visitor):
    def visitParentheses(self, ctx):
        # skip parentheses
        return self.visit(ctx.expr())

    def visitTerminal(self, ctx):
        return ctx.getText()

    hoof.register("Prog", Program, ["expr->body"])            # no config on node
    hoof.register("BinaryExpr", BinaryExpr)                   # no need to remap
    hoof.register(RunExpr)                                    # rule and remap on node

hoof.bind(AstVisitor)


def test_program():
    node = hoof.parse("1 + 2; 3 - 4;", "prog")
    assert isinstance(node, Program)
    assert len(node.body) == 2
    assert isinstance(node.body[0], BinaryExpr)

def test_binary():
    node = hoof.parse("1 + 2", "expr")
    assert isinstance(node, BinaryExpr)
    assert node.left == "1"
    assert node.right == "2"
    assert node.op == "+"

def test_put():
    node = hoof.parse("run 2", "expr")
    assert isinstance(node, RunExpr)
    assert node.expr == "2"

def test_parentheses():
    node = hoof.parse("(1 + 1)", "expr")
    assert isinstance(node, BinaryExpr)

def test_expr_integer():
    # this is a Token (INT) with no explicit shaping, so is result of visitTerminal
    node = hoof.parse("1", "expr")
    node == "1"


