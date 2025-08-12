from typing import Dict, Any
import os


def mcp_config() -> Dict[str, Any]: 

    tavily_api_key = os.getenv("TAVILY_API_KEY")

    #add additional mcp servers here as needed
    
    return {
        "tavily": {
            "command": "npx",
            "args": ["-y", "mcp-remote", f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}"]
        }
    }


