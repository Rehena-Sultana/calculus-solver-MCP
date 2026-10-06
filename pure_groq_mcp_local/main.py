import argparse
from client import solve_question

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculus Solver CLI (Pure Groq + MCP)")
    parser.add_argument(
        "--mode",
        choices=["local", "remote"],
        default="local",
        help="MCP connection mode: 'local' (stdio subprocess) or 'remote' (SSE URL)",
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/sse",
        help="SSE server URL when using --mode remote",
    )
    args = parser.parse_args()

    question = input("Enter your calculus question: ")
    print(f"\nConnecting via {args.mode.upper()} MCP & Solving with Groq...\n")
    print(solve_question(question, mode=args.mode, sse_url=args.url if args.mode == "remote" else None))
