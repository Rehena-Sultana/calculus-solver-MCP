import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

# Robust .env loading (current directory or parent)
local_env = Path(__file__).parent / ".env"
parent_env = Path(__file__).parent.parent / ".env"
if local_env.exists():
    load_dotenv(dotenv_path=local_env)
if parent_env.exists():
    load_dotenv(dotenv_path=parent_env)

async def _execute_with_session(session: ClientSession, client: Groq, model: str, question: str) -> str:
    """Core tool-calling loop using an established MCP session."""
    # 1. Initialize MCP protocol handshake
    await session.initialize()

    # 2. Dynamically discover tools from the MCP server
    tools_list = await session.list_tools()
    
    # Map MCP tool definitions to Groq / OpenAI tool format
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

    # 3. Request completion with discovered MCP tools
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=groq_tools if groq_tools else None,
        tool_choice="auto" if groq_tools else None,
        temperature=0,
    )

    response_message = response.choices[0].message

    # 4. Handle tool execution via MCP session
    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # Delegate tool execution to the MCP Server
            mcp_result = await session.call_tool(tool_name, arguments=tool_args)
            
            # Extract content from MCP tool response
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

        # 5. Get final formatted explanation from Groq
        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return final_response.choices[0].message.content

    return response_message.content

async def run_mcp_solver(question: str, mode: str = "local", sse_url: Optional[str] = None) -> str:
    """Run calculus solver over Local MCP (stdio) or Remote MCP (SSE)."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    if mode == "remote" and sse_url:
        # Remote MCP via SSE transport over network/internet
        async with sse_client(sse_url) as (read, write):
            async with ClientSession(read, write) as session:
                return await _execute_with_session(session, client, model, question)
    else:
        # Local MCP via stdio subprocess on the local machine
        server_path = Path(__file__).parent / "server.py"
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(server_path)],
            env=os.environ.copy(),
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                return await _execute_with_session(session, client, model, question)

def solve_question(question: str, mode: str = "local", sse_url: Optional[str] = None) -> str:
    """Synchronous entry point for the MCP solver."""
    return asyncio.run(run_mcp_solver(question, mode=mode, sse_url=sse_url))
