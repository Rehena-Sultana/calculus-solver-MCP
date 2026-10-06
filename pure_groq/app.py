'''
User types/clicks a question → AI (Groq) reads it and decides it needs real math → AI calls solve_calculus → SymPy computes the exact answer → that answer is fed back to the AI → AI writes a clear explanation using the correct number → Streamlit displays it.
'''
import json
import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import sympy as sp

# -------------------------------------------------------------
# 1. Environment & Setup
# -------------------------------------------------------------
load_dotenv()

# -------------------------------------------------------------
# 2. SymPy Symbolic Math Tool
# -------------------------------------------------------------
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

# Tool definition for Groq native tool calling -->Describing the Tool to the AI
# This is not code that runs math — it's a JSON "spec sheet" describing the solve_calculus function to the AI model
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

# -------------------------------------------------------------
# 3. Pure Groq Tool Calling Solver
# -------------------------------------------------------------
def solve_question(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")
    # Creates a client object to communicate with Groq's servers, using the API key
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

    # Handle tool calls if requested by Groq
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

        # Get final explanation from Groq with tool result
        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return final_response.choices[0].message.content

    return response_message.content

# -------------------------------------------------------------
# 4. Streamlit User Interface
# -------------------------------------------------------------
st.set_page_config(page_title="Calculus Solver (Pure Groq)", page_icon="∫", layout="centered")

st.title("∫ Calculus Solver")
# st.caption("⚡ Powered by Pure Groq Tool Calling + SymPy (No LangChain)")
st.write("Ask any calculus question and get a step-by-step symbolic solution.")

# Initialize session state for input
if "question_input" not in st.session_state:
    st.session_state["question_input"] = ""

st.markdown("##### 💡 Try an Example:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📐 **Derivative**\n\n$x^3 + 2x^2 - 5x$", use_container_width=True):
        st.session_state["question_input"] = "Find the derivative of x^3 + 2*x^2 - 5*x"

with col2:
    if st.button("∫ **Integral**\n\n$6x^2 + 4x - 3$", use_container_width=True):
        st.session_state["question_input"] = "Calculate the indefinite integral of 6*x^2 + 4*x - 3 dx"

with col3:
    if st.button("🎯 **Limit**\n\n$\\lim_{x \\to 0} \\frac{\\sin(x)}{x}$", use_container_width=True):
        st.session_state["question_input"] = "Find the limit of sin(x)/x as x approaches 0"

question = st.text_area(
    "Enter your calculus question:",
    value=st.session_state["question_input"],
    placeholder="Example: Find the derivative of x^3 + 2*x^2 - 5*x",
    height=100,
)

if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question or click an example above.")
    else:
        with st.spinner("Solving with Groq & SymPy..."):
            try:
                answer = solve_question(question)
                st.markdown("---")
                st.markdown("### 📝 Step-by-Step Solution")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {e}")

