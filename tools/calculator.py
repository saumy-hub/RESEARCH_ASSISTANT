import ast
import operator
import math
from rich.console import Console

console = Console()

# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Supported functions
FUNCTIONS = {
    'sqrt': math.sqrt,
    'log': math.log,
    'sin': math.sin,
    'cos': math.cos,
    'abs': abs,
    'round': round
}

def safe_eval(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.Constant): # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise TypeError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        op = OPERATORS[type(node.op)]
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return op(left, right)
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        op = OPERATORS[type(node.op)]
        operand = safe_eval(node.operand)
        return op(operand)
    elif isinstance(node, ast.Call): # Function calls
        if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS:
            func = FUNCTIONS[node.func.id]
            args = [safe_eval(arg) for arg in node.args]
            return func(*args)
        else:
            raise ValueError(f"Unsupported function call: {ast.unparse(node.func) if hasattr(ast, 'unparse') else 'unknown'}")
    elif isinstance(node, ast.Expression):
        return safe_eval(node.body)
    else:
        raise TypeError(f"Unsupported AST node type: {type(node)}")

def calculate(expression: str) -> dict:
    try:
        console.log(f"Calculating: [bold magenta]{expression}[/bold magenta]")
        # Parse the expression
        node = ast.parse(expression, mode='eval')
        result = safe_eval(node.body)
        console.log(f"Result: {result}")
        return {"expression": expression, "result": result}
    except Exception as e:
        console.log(f"[red]Error evaluating expression: {e}[/red]")
        return {"error": f"unsafe expression or evaluation error: {str(e)}"}
