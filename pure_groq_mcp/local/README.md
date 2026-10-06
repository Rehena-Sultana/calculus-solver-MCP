# Local Model Context Protocol (MCP) — Calculus Solver

A standalone implementation of **Local MCP** using standard input/output (`stdio`) process pipes.

## How it Works
1. `server.py` is the FastMCP server that exposes SymPy calculus tools.
2. `client.py` launches `server.py` as a local subprocess, discovers tools over `stdio`, and binds them to the Groq LLM.
3. No network ports, URLs, or firewalls needed.

## Running
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Streamlit Web App
streamlit run app.py

# Or run CLI
python main.py
```
