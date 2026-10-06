import sympy as sp
from mcp.server.mcpserver import MCPServer

# Initialize Local MCP Server
mcp = MCPServer("Calculus-Local-MCP-Server")

@mcp.tool()
def solve_calculus(expression: str, operation: str) -> str:
    """Perform symbolic calculus operations using SymPy.
    
    Args:
        expression: A mathematical expression in terms of x (e.g. 'x^3 + 2*x^2 - 5*x', 'sin(x)*cos(x)')
        operation: Calculus operation to perform: 'derivative', 'integral', 'limit', 'simplify', or 'solve'
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
            return f"Unsupported operation: {operation}. Use derivative, integral, limit, simplify, or solve."

        return str(result)
    except Exception as e:
        return f"SymPy computation error: {e}"

if __name__ == "__main__":
    # Local transport over standard input/output pipes
    mcp.run(transport="stdio")
