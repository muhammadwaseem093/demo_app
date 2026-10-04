"""Pure calculator engine (no Streamlit)."""

from __future__ import annotations

import ast
import math
import operator
import re
from typing import Any

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def build_functions(angle_mode: str) -> dict[str, Any]:
    use_deg = angle_mode == "DEG"

    def _trig(fn: Any, x: float) -> float:
        arg = math.radians(x) if use_deg else x
        return fn(arg)

    def _inv_trig(fn: Any, x: float) -> float:
        val = fn(x)
        return math.degrees(val) if use_deg else val

    return {
        "sin": lambda x: _trig(math.sin, x),
        "cos": lambda x: _trig(math.cos, x),
        "tan": lambda x: _trig(math.tan, x),
        "asin": lambda x: _inv_trig(math.asin, x),
        "acos": lambda x: _inv_trig(math.acos, x),
        "atan": lambda x: _inv_trig(math.atan, x),
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "exp": math.exp,
        "abs": abs,
        "factorial": math.factorial,
        "pi": math.pi,
        "e": math.e,
    }


class SafeEvaluator(ast.NodeVisitor):
    def __init__(self, functions: dict[str, Any]) -> None:
        self._functions = functions

    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    def visit_Num(self, node: ast.Num) -> Any:  # noqa: N802 — Py<3.14 compat
        return node.n

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        op = _UNARYOPS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        return op(self.visit(node.operand))

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero")
        return op(left, right)

    def visit_Call(self, node: ast.Call) -> Any:
        if node.keywords or not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        name = node.func.id
        if name not in self._functions:
            raise ValueError(f"Unknown function: {name}")
        fn = self._functions[name]
        if name in ("pi", "e"):
            if node.args:
                raise ValueError(f"{name} takes no arguments")
            return fn
        if len(node.args) != 1:
            raise ValueError(f"{name}() expects one argument")
        arg = self.visit(node.args[0])
        if name == "factorial":
            if not isinstance(arg, (int, float)) or arg < 0 or arg != int(arg):
                raise ValueError("factorial() requires a non-negative integer")
            arg = int(arg)
        return fn(arg)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in ("pi", "e"):
            return self._functions[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    def generic_visit(self, node: ast.AST) -> Any:
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def auto_close_parentheses(expr: str) -> str:
    """Append missing ')' so sin(90 or sqrt(16 evaluate without manual closing."""
    missing = expr.count("(") - expr.count(")")
    if missing <= 0:
        return expr
    return expr + ")" * missing


def normalize_expression(expr: str, last_answer: float) -> str:
    text = expr.strip()
    replacements = {
        "×": "*",
        "÷": "/",
        "^": "**",
        "mod": "%",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\bANS\b", str(last_answer), text)


def evaluate_expression(expr: str, angle_mode: str, last_answer: float) -> float:
    if not expr.strip():
        raise ValueError("Empty expression")
    closed = auto_close_parentheses(expr.strip())
    normalized = normalize_expression(closed, last_answer)
    tree = ast.parse(normalized, mode="eval")
    result = SafeEvaluator(build_functions(angle_mode)).visit(tree)
    if isinstance(result, (int, float)):
        if not math.isfinite(result):
            raise ValueError("Result is not finite")
        return float(result)
    raise ValueError("Invalid result")


def format_result(value: float) -> str:
    if abs(value) >= 1e12 or (abs(value) < 1e-6 and value != 0):
        return f"{value:.6e}"
    rounded = round(value, 10)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded).rstrip("0").rstrip(".")
