import streamlit as st
from client import solve_question

st.set_page_config(page_title="Calculus Solver (Local MCP)", page_icon="∫", layout="centered")

st.title("∫ Calculus Solver")
st.caption("🔒 Powered by Pure Groq + Local MCP (`stdio` Subprocess) + SymPy")
st.write("Ask any calculus question. Tools are executed locally via **Local Model Context Protocol**.")

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

if st.button("🚀 Solve with Local MCP", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question or click an example above.")
    else:
        with st.spinner("Executing Local MCP Server & Solving with Groq..."):
            try:
                answer = solve_question(question)
                st.markdown("---")
                st.markdown("### 📝 Step-by-Step Solution")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error: {e}")
