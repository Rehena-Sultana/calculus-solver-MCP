import json
import os
from dotenv import load_dotenv
from groq import Groq
import sympy as sp

load_dotenv()

def solve_calculus(expression: str, operation: str) -> str:
    """Performs symbolic calculus operations using SymPy."""
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

CALCULUS_TOOL = {
    "type": "function",
    "function": {
        "name": "solve_calculus",
        "description": "Perform symbolic calculus operations on mathematical expressions using SymPy.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression in terms of variable x (e.g. 'x**3 + 2*x**2 - 5*x', 'sin(x)*cos(x)')",
                },
                "operation": {
                    "type": "string",
                    "enum": ["derivative", "integral", "limit", "simplify", "solve"],
                    "description": "Calculus operation to perform.",
                },
            },
            "required": ["expression", "operation"],
        },
    },
}

def solve_question(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

    client = Groq(api_key=api_key.strip())
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert calculus tutor.\n"
                "Solve calculus questions accurately and explain each step clearly.\n"
                "Always use the solve_calculus tool for symbolic calculations (derivatives, integrals, limits, equations).\n"
                "Do not invent calculation results. Provide a clear final answer."
            ),
        },
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[CALCULUS_TOOL],
        tool_choice="auto",
        temperature=0,
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            tool_result = solve_calculus(
                expression=args.get("expression", ""),
                operation=args.get("operation", ""),
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": tool_result,
            })

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return final_response.choices[0].message.content

    return response_message.content

if __name__ == "__main__":
    question = input("Enter your calculus question: ")
    print("\nSolving with Pure Groq + SymPy...\n")
    print(solve_question(question))
