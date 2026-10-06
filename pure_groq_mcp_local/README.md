# Pure Groq + Dual-Mode Model Context Protocol (MCP)

Calculus solver supporting **both Local MCP (`stdio`)** and **Remote MCP (`SSE`)** using the official Python MCP SDK and Groq Cloud.

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit UI / CLI                              │
│         (Sidebar Switch: Local 'stdio' vs Remote 'sse')                │
└──────────────────┬──────────────────────────────────┬──────────────────┘
                   │ (stdio transport)                │ (HTTP SSE transport)
                   ▼                                  ▼
      ┌─────────────────────────┐        ┌─────────────────────────┐
      │   Local MCP Server      │        │   Remote MCP Server     │
      │   (server.py process)   │        │   (http://.../sse)      │
      └────────────┬────────────┘        └────────────┬────────────┘
                   │                                  │
                   └─────────────────┬────────────────┘
                                     ▼
                              [SymPy Engine]
                                     │
                             (Results returned)
                                     ▼
                              [Groq LLM Brain]
```

---

## Running

### 1. Launch the Streamlit Web UI:
```bash
cd pure_groq_mcp
streamlit run app.py
```
* **Local Mode (Default):** Works immediately with zero extra steps.
* **Remote SSE Mode:** Toggle the sidebar to **Remote MCP (SSE)**.

---

### 2. How to Test Remote SSE Mode:

1. In a separate terminal, start the MCP Server in SSE mode:
   ```bash
   python server.py --transport sse --port 8000
   ```
   *(Server starts at `http://127.0.0.1:8000/sse`)*

2. In your Streamlit app sidebar, select **Remote MCP (SSE)** and solve questions!

---

### 3. Deploying to Render:

* **Single Container (Recommended for beginners):** Deploy the Streamlit app to Render. It will automatically run in **Local MCP (`stdio`)** mode inside the Render container with zero setup!
* **Separate Microservice:** Deploy `server.py` with `python server.py --transport sse --host 0.0.0.0 --port $PORT` to Render, and connect to `https://your-mcp-service.onrender.com/sse`.
