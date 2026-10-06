import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import solve_calculus

load_dotenv()

SYSTEM_PROMPT = """You are a calculus tutor.
Solve calculus questions accurately and explain the solution step by step.
Use the SymPy tool for symbolic calculations whenever appropriate.
Do not invent calculation results.
Explain the final answer clearly in simple language."""

def build_agent():
    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY", "").strip(),
    )

    tools = [solve_calculus]
    return create_agent(model, tools, system_prompt=SYSTEM_PROMPT)

def solve_question(question: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    last_message = result["messages"][-1]
    if isinstance(last_message.content, str):
        return last_message.content
    elif isinstance(last_message.content, list):
        text_parts = [
            part if isinstance(part, str) else part.get("text", "")
            for part in last_message.content
            if isinstance(part, (str, dict))
        ]
        return "\n".join(text_parts)
    return str(last_message.content)

