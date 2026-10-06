# Pure Groq Model Context Protocol (MCP)

This directory contains two dedicated implementations of MCP:

```
pure_groq_mcp/
├── local/      # 🔒 Local MCP (stdio subprocess pipes, zero network needed)
└── remote/     # 🌐 Remote MCP (HTTP Server-Sent Events / SSE across networks)
```

---

## 1. `local/` (Local MCP — stdio)
* Runs `server.py` as an automatic local child process.
* **Run:**
  ```bash
  cd local
  streamlit run app.py
  ```

---

## 2. `remote/` (Remote MCP — SSE)
* Runs `server.py` as an HTTP Web Server.
* Connects `client.py` and `app.py` over the network via `sse_client`.
* **Run:**
  ```bash
  cd remote
  python server.py          # Terminal 1 (Starts server on port 8000)
  streamlit run app.py      # Terminal 2 (Starts Web UI)
  ```
