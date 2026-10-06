# Remote Model Context Protocol (MCP) — Calculus Solver

A standalone implementation of **Remote MCP** communicating over HTTP Server-Sent Events (`SSE`).

## Architecture
1. **`server.py`**: Runs as a standalone HTTP server on `http://127.0.0.1:8000/sse` (or deployed to Render/cloud).
2. **`client.py`**: Connects to the remote server over network/internet via `sse_client`.

## Running Locally

### Step 1: Start the Remote MCP Server
```bash
python server.py
```
*(Starts listening at `http://127.0.0.1:8000/sse`)*

### Step 2: Run the Web App or CLI (in another terminal)
```bash
# Web UI
streamlit run app.py

# Or CLI
python main.py
```

## Deploying to Render
1. Deploy `server.py` to Render as a Web Service.
2. Start Command: `python server.py` (it will bind to `$PORT`).
3. Point your `app.py` to your Render URL: `https://your-server.onrender.com/sse`.
