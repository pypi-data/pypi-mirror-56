from .Operator import DvOperator


class Condition(object):
    def __init__(self, left_expr, operator: DvOperator, right_expr):
        self.operator = operator
        self.left = left_expr
        self.right = right_expr

    def text(self):
        if self.left is None or self.right is None:
            return None
        return self.build(self.left)+self.operator.value+self.build(self.right)

    def build(self, expr):
        if type(expr).__name__ != "Condition":
            return expr
        else:
            return "({left} {operator} {right})".format(left=self.build(expr.left), operator=expr.operator.value, right=self.build(expr.right))

    def get(self, expr, key):
        if type(expr).__name__ != "Condition":
            return None
        if key == expr.left:
            return expr
        if key == expr.right:
            return expr

        node = self.get(expr.left, key)
        if node is not None:
            return node
        else:
            node = self.get(expr.right, key)
        return node

    def del_expr(self, expr):
        pass
