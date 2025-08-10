from mcp import mcp_config
from mcp.client import MCPClient
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional
from contextlib import AsyncExitStack
from mcp.client.sse import sse_client

async def setup_mcp_servers() -> MCPClient:
    mcpclient = MCPClient()
    server_config = mcp_config()

    for server_name, config in server_config.items():
        await mcpclient.connect_to_server(server_name, config)

    return mcpclient

