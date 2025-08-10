import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional
from contextlib import AsyncExitStack
from mcp.client.sse import sse_client

class MCPClient():
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.available_tools = {}
        self.sessions = {}

    async def connect_to_server(self, server_name, server_config):
        try: 

            if server_config.get("type") == "http":
                url = server_config["url"]
                headers = {}

                if "token" in server_config:
                    headers["Authorization"] = f"Bearer {server_config['token']}"
                elif "headers" in server_config:
                    headers.update(server_config["headers"])

                transport = await self.exit_stack.enter_async_context(
                        sse_client(url, headers=headers)
                    )

            else:
                
                server_params = StdioServerParameters(
                    command = server_config["command"],
                    args = server_config.get("args", []),
                    env = server_config.get("env", {})
                )

                transport = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                
        
            self.stdio, self.write = transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

            await self.session.initialize()

            tools_list = await self.session.list_tools()

            self.sessions[server_name] = self.session
            
            for tool in tools_list.tools:
                self.available_tools[tool.name] = {
                    "server": server_name,
                    "tool": tool
                }

            print(f"connected to {server_name}, available tools: {[tool.name for tool in tools_list.tools]}")

        except Exception as e:
            print(f"Failed to connect to MCP server {server_name}: {e}")
            return


    async def execute_mcp_tool(self, tool_name, arguments):
        
        if tool_name not in self.available_tools:
            return f"Tool {tool_name} not in the MCP server"

        tool_info = self.available_tools[tool_name]
        server_name = tool_info["server"]
        session = self.sessions[server_name]

        try:
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else "No result"

        except Exception as e: 
            return f"Error executing mcp tool: {e}"   