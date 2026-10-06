import argparse
from client import solve_question

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remote MCP Calculus Solver CLI")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/sse",
        help="URL of the running Remote MCP Server",
    )
    args = parser.parse_args()

    question = input("Enter your calculus question: ")
    print(f"\nConnecting to Remote MCP ({args.url}) & Solving with Groq...\n")
    print(solve_question(question, sse_url=args.url))
