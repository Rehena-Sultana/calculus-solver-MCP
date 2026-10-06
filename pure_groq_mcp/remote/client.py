import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession
from mcp.client.sse import sse_client

# Robust .env loading
local_env = Path(__file__).parent / ".env"
parent_env = Path(__file__).parent.parent.parent / ".env"
if local_env.exists():
    load_dotenv(dotenv_path=local_env)
if parent_env.exists():
    load_dotenv(dotenv_path=parent_env)

async def run_remote_mcp_solver(question: str, sse_url: str = "http://127.0.0.1:8000/sse") -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    # Connect to Remote MCP Server over network/internet via SSE
    async with sse_client(sse_url) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize MCP handshake
            await session.initialize()

            # 2. Discover tools dynamically from remote MCP server
            tools_list = await session.list_tools()
            
            groq_tools = []
            for t in tools_list.tools:
                schema = getattr(t, "input_schema", getattr(t, "inputSchema", {}))
                groq_tools.append({
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": schema,
                    },
                })

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an expert calculus tutor.\n"
                        "Solve calculus questions accurately and explain each step clearly.\n"
                        "Always use the available solve_calculus MCP tool for exact symbolic calculations.\n"
                        "Do not invent calculation results. Provide a clear final answer."
                    ),
                },
                {"role": "user", "content": question},
            ]

            # 3. Call Groq with remote MCP tools
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=groq_tools if groq_tools else None,
                tool_choice="auto" if groq_tools else None,
                temperature=0,
            )

            response_message = response.choices[0].message

            # 4. Handle tool execution via remote MCP server
            if response_message.tool_calls:
                messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    mcp_result = await session.call_tool(tool_name, arguments=tool_args)
                    
                    tool_content = ""
                    for content_item in mcp_result.content:
                        if hasattr(content_item, "text"):
                            tool_content += content_item.text
                        else:
                            tool_content += str(content_item)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_content,
                    })

                # 5. Get final response from Groq
                final_response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0,
                )
                return final_response.choices[0].message.content

            return response_message.content

def solve_question(question: str, sse_url: str = "http://127.0.0.1:8000/sse") -> str:
    """Synchronous entry point for Remote MCP solver."""
    return asyncio.run(run_remote_mcp_solver(question, sse_url=sse_url))
