from langchain_core.tools import tool
import sympy as sp

@tool
def solve_calculus(expression: str, operation: str) -> str:
    """Perform symbolic calculus using SymPy.
    operation: derivative, integral, limit, simplify, or solve.
    expression: a SymPy-compatible expression.
    """
    try:
        x = sp.Symbol("x")
        clean_expr = expression.replace("^", "**")
        expr = sp.sympify(clean_expr)
        op = operation.lower().strip()

        if op == "derivative":
            result = sp.diff(expr, x)
        elif op == "integral":
            result = sp.integrate(expr, x)
        elif op == "limit":
            result = sp.limit(expr, x, 0)
        elif op == "simplify":
            result = sp.simplify(expr)
        elif op == "solve":
            result = sp.solve(expr, x)
        else:
            return f"Unsupported operation: {operation}"

        return str(result)
    except Exception as e:
        return f"Could not calculate: {e}"
