'''
open an separate terminal and myenv then write python server.py --transport sse, to run remote MCP, we have to open two terminals at a time. 1. streamlit, 2.python server.py --transport sse

'''

import argparse
import sympy as sp
from mcp.server.mcpserver import MCPServer

# Initialize MCP Server (MCP 2.x API)
mcp = MCPServer("Calculus-MCP-Server")

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
    parser = argparse.ArgumentParser(description="Calculus MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport mode: 'stdio' (for local subprocess) or 'sse' (for remote web service)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host address for SSE server")
    parser.add_argument("--port", type=int, default=8000, help="Port number for SSE server")
    args = parser.parse_args()

    if args.transport == "sse":
        print(f"[*] Starting Remote Calculus MCP Server (SSE) on http://{args.host}:{args.port}/sse")
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
