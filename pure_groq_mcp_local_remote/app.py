import streamlit as st
from client import solve_question

st.set_page_config(page_title="Calculus Solver (Dual-Mode MCP)", page_icon="∫", layout="wide")

# -------------------------------------------------------------
# 1. Sidebar: MCP Connection Settings
# -------------------------------------------------------------
st.sidebar.title("⚙️ MCP Settings")
st.sidebar.caption("Choose how your AI connects to the MCP Tool Server.")

transport_mode = st.sidebar.radio(
    "🔌 Connection Mode:",
    options=["Local MCP (stdio)", "Remote MCP (SSE)"],
    index=0,
    help="Local uses direct subprocess pipe on your machine. Remote connects over HTTP/network.",
)

if transport_mode == "Local MCP (stdio)":
    selected_mode = "local"
    sse_url = None
    st.sidebar.success("🟢 **Mode: Local Subprocess**")
    st.sidebar.info("Launches `server.py` automatically as a local process via standard input/output (`stdio`).")
else:
    selected_mode = "remote"
    st.sidebar.info("🔵 **Mode: Remote SSE**\n\nConnect to an MCP Server running over the network or cloud.")
    sse_url = st.sidebar.text_input(
        "SSE Server URL:",
        value="http://127.0.0.1:8000/sse",
        help="URL of your running SSE MCP Server (e.g. http://127.0.0.1:8000/sse or Render URL).",
    )
    st.sidebar.markdown(
        """
        > **💡 How to run local SSE server:**
        > ```bash
        > python server.py --transport sse
        > ```
        """
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 About MCP")
st.sidebar.write(
    "**Model Context Protocol (MCP)** provides a standard interface for LLMs to discover and invoke tools, whether running locally or in the cloud."
)

# -------------------------------------------------------------
# 2. Main Page UI
# -------------------------------------------------------------
st.title("∫ Calculus Solver")
st.caption(f"Powered by Pure Groq + Model Context Protocol ({transport_mode}) + SymPy")
st.write("Ask any calculus question and get an exact, step-by-step symbolic math solution.")

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

button_label = f"🚀 Solve with {transport_mode}"
if st.button(button_label, type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question or click an example above.")
    else:
        spinner_msg = (
            "Connecting to Local MCP Server & Solving..."
            if selected_mode == "local"
            else f"Connecting to Remote MCP ({sse_url}) & Solving..."
        )
        with st.spinner(spinner_msg):
            try:
                answer = solve_question(question, mode=selected_mode, sse_url=sse_url)
                st.markdown("---")
                st.markdown("### 📝 Step-by-Step Solution")
                st.markdown(answer)
            except Exception as e:
                st.error(f"Error ({transport_mode}): {e}")
                if selected_mode == "remote":
                    st.info("Make sure your SSE server is running: `python server.py --transport sse`")
