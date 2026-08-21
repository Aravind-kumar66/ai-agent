import ast
import operator


# Allowed mathematical operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Examples:
        10 + 5
        20 * 4
        100 / 5
        2 ** 10
    """

    try:
        tree = ast.parse(expression, mode="eval")

        result = _evaluate(tree.body)

        return str(result)

    except Exception as e:
        return f"Calculator error: {e}"


def _evaluate(node):

    # Numbers
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    # Binary operations
    if isinstance(node, ast.BinOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Operator not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return OPERATORS[type(node.op)](left, right)

    # Negative numbers
    if isinstance(node, ast.UnaryOp):

        if type(node.op) not in OPERATORS:
            raise ValueError("Operator not allowed.")

        operand = _evaluate(node.operand)

        return OPERATORS[type(node.op)](operand)

    raise ValueError("Invalid mathematical expression.")

if __name__ == "__main__":
    print(calculate("25 * 48"))
    print(calculate("100 / 4"))
    print(calculate("2 ** 10"))