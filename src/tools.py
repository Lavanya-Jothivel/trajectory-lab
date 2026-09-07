import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_evaluate(node.operand))

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Safely evaluate a basic mathematical expression."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)
    except Exception as error:
        return f"Calculator error: {error}"
    
KNOWLEDGE_BASE = {
    "capital of france": "Paris",
    "capital of japan": "Tokyo",
    "creator of python": "Guido van Rossum",
}


def lookup(query: str) -> str:
    """Look up a fact from a small local knowledge base."""
    key = query.strip().lower()

    if key in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[key]

    return f"No result found for: {query}"
def unreliable_calculator(expression: str) -> str:
    """
    Calculator used for failure-recovery experiments.

    Expressions containing 15 intentionally simulate
    a temporary tool failure.
    """
    if "15" in expression:
        return "ERROR: calculator temporarily unavailable"

    return calculator(expression)
def faulty_calculator(expression: str) -> str:
    """
    Calculator for verification experiments.

    It silently returns an incorrect answer for expressions
    containing '8 * 8', without reporting an error.
    """

    normalized = expression.replace(" ", "")

    if "8*8" in normalized:
        return "63"

    return calculator(expression)


TOOLS = {
    "calculator": calculator,
    "unreliable_calculator": unreliable_calculator,
    "faulty_calculator": faulty_calculator,
    "lookup": lookup,
}


def run_tool(tool_name: str, tool_input: str) -> str:
    """Run a registered tool by name."""
    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    return tool(tool_input)