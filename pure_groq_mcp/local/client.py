import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Robust .env loading
local_env = Path(__file__).parent / ".env" # check .env and current file locate at the same folder.
parent_env = Path(__file__).parent.parent.parent / ".env" # goes up 3 levels up to root folder check .env and current file locate at 3 folder upper than current folder.
if local_env.exists():
    load_dotenv(dotenv_path=local_env)
if parent_env.exists():
    load_dotenv(dotenv_path=parent_env)

async def run_local_mcp_solver(question: str) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    # Local server.py path
    server_path = Path(__file__).parent / "server.py"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize MCP handshake
            await session.initialize()

            # 2. Discover tools dynamically from local MCP server
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

            # 3. Call Groq with MCP tools
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=groq_tools if groq_tools else None,
                tool_choice="auto" if groq_tools else None,
                temperature=0,
            )

            response_message = response.choices[0].message

            # 4.  toolHandle execution via local MCP server
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

def solve_question(question: str) -> str:
    """Synchronous entry point for Local MCP solver."""
    return asyncio.run(run_local_mcp_solver(question))
