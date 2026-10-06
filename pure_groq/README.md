# Pure Groq Calculus Solver (No LangChain)

A lightweight, single-script calculus solver powered directly by the **Groq Python SDK** and **SymPy** for exact symbolic mathematics.

## Features
- **Zero LangChain overhead**: Uses native OpenAI-compatible Groq tool calling.
- **Fast & Lightweight**: Minimal dependencies (`groq`, `sympy`, `python-dotenv`, `streamlit`).
- **All-in-one Single Scripts**: Everything you need in a single file.

## Requirements
```bash
pip install -r requirements.txt
```

## Running

1. Make sure your `GROQ_API_KEY` is in the root `.env` file.
2. **Streamlit Web UI**:
   ```bash
   streamlit run app.py
   ```
3. **Terminal / CLI**:
   ```bash
   python main.py
   ```
