# Calculus Solver (LangChain + Groq)

Calculus problem solver built using **LangChain tool calling**, **Groq LLM**, and **SymPy** for exact symbolic mathematics.

## Requirements
```bash
pip install -r requirements.txt
```

## Setup
1. Copy `.env.example` to `.env` (or use the root `.env`).
2. Add your Groq API key:
   ```env
   GROQ_API_KEY=your_key_here
   GROQ_MODEL=openai/gpt-oss-120b
   ```

## Running
* **Streamlit Web UI:**
  ```bash
  streamlit run app.py
  ```
* **Terminal / CLI:**
  ```bash
  python main.py
  ```
