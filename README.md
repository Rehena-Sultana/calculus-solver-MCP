# Calculus Solver Project

Three complete implementations of an AI-powered Calculus Problem Solver using Groq and SymPy:

```
calculus-solver-without-mcp/
│
├── pure_groq/                  # ⚡ Direct Pure Groq SDK + SymPy (No MCP, No LangChain)
│
├── langchain_groq/             # 🦜️🔗 LangChain Agent Architecture + SymPy
│
└── pure_groq_mcp/              # 🔌 Model Context Protocol (MCP) Architectures
    ├── local/                  # 🔒 Local MCP (stdio subprocess pipes, zero network)
    └── remote/                 # 🌐 Remote MCP (HTTP Server-Sent Events / SSE)
```

---

## 1. `pure_groq/` (Direct Tool Calling)
* Ultra-lightweight, single-script solution with zero framework overhead.
* **Run:**
  ```bash
  cd pure_groq
  pip install -r requirements.txt
  streamlit run app.py
  ```

---

## 2. `langchain_groq/` (LangChain Agent)
* Full LangChain agent ecosystem using `ChatGroq` and `@tool` decorators.
* **Run:**
  ```bash
  cd langchain_groq
  pip install -r requirements.txt
  streamlit run app.py
  ```

---

## 3. `pure_groq_mcp/` (Model Context Protocol)

### 🔒 Local MCP (`pure_groq_mcp/local/`):
* Standard input/output (`stdio`) process communication.
* **Run:**
  ```bash
  cd pure_groq_mcp/local
  pip install -r requirements.txt
  streamlit run app.py
  ```

### 🌐 Remote MCP (`pure_groq_mcp/remote/`):
* HTTP Server-Sent Events (`SSE`) transport over the network.
* **Run:**
  ```bash
  cd pure_groq_mcp/remote
  pip install -r requirements.txt
  python server.py          # Terminal 1: Starts SSE Server
  streamlit run app.py      # Terminal 2: Launches Web UI
  ```
