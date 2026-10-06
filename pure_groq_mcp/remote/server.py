import os
import sympy as sp
from mcp.server.mcpserver import MCPServer

# Initialize Remote MCP Server
mcp = MCPServer("Calculus-Remote-MCP-Server")

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
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"[*] Starting Remote MCP Server (SSE) on http://{host}:{port}/sse")
    # Remote transport over HTTP Server-Sent Events (SSE)
    mcp.run(transport="sse", host=host, port=port)
