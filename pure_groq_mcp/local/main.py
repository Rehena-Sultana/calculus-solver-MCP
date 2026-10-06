from client import solve_question

if __name__ == "__main__":
    question = input("Enter your calculus question: ")
    print("\nConnecting to Local MCP Server (stdio) & Solving with Groq...\n")
    print(solve_question(question))
