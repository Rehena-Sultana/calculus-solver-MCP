from agent import solve_question

if __name__ == "__main__":
    question = input("Enter your calculus question: ")
    print("\nSolving with LangChain + Groq + SymPy...\n")
    print(solve_question(question))
