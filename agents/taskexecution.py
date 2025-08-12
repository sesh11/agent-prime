from util.utility import invoke_claude, invoke_claude_with_tools
from mcp_local.mcp_setup import setup_mcp_servers
import textwrap
import anthropic
import os

class TaskExecutionAgent:
    def __init__(self, task: str, prev_tasks_responses: list):
        self.task = task
        self.prev_tasks_responses = prev_tasks_responses
        pass

    async def task_execution(self):
        
        string_prev_task_responses = "".join(self.prev_tasks_responses)
        prompt = textwrap.dedent("""
        You are an extremely helpful assistant that has access to web search, analysis, and scheduling tools. Use tools when you need additional information or when the task requires data or actions from external sources. 
        The task is defined as follows: 
        {{Task}}
        For reference, you are also provided with the tasks that were executed prior to this specific task and their associated responses. 
        {{prev_tasks_responses}}

        IMPORTANT: Use the prev_tasks_responses as a helpful input to determine the right tools that need to be called.  
        """).replace("{{Task}}", self.task).replace("{{prev_tasks_responses}}", string_prev_task_responses)

        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        claude_tools = []

        mcp_executor = await setup_mcp_servers()

        #assign tools from an mcp server to Claude Tools
        #In order to do this, you need a method that can provide a list of tools. 
        #For that you need a method that can connect to a set of mcp servers and return an object
        #you need to create an object and assign it the mcp server connections
        #use that object.method name i.e. available tools to get it
        
        system_prompt = textwrap.dedent("""
        You are an extremely helpful assistant that is also an expert in using tools. You don't execute any additional tasks other than what is provided to you.
        You are focused on completing the task and find the shortest and most efficient path to completing the task and getting to the answer.
        """)

        try: 
            
            for tool_name, tool_info in mcp_executor.available_tools.items():
                tool_def = tool_info["tool"]
                claude_tools.append({
                    "name": tool_name,
                    "description": tool_def.description,
                    "input_schema": tool_def.inputSchema
                })
            
            messages = [
                        {"role": "user", "content": prompt}
                    ]
            
            while True: 
                response = invoke_claude_with_tools(model="claude-sonnet-4-20250514", messages=messages, system_prompt=system_prompt, claude_tools=claude_tools, max_tokens=1024)
    
                messages.append({"role": "assistant", "content": response.content})
        
                if response.stop_reason == "tool_use":
                    tools_results = []
    
                    for contentblock in response.content:
                        if contentblock.type == "tool_use":
                            tool_name = contentblock.name
                            tool_input = contentblock.input
                            tool_id = contentblock.id
    
                            print(f"Executing MCP Tool {tool_name} with {tool_input}")
    
                            result = await mcp_executor.execute_mcp_tool(tool_name, tool_input)
    
                            tools_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": result
                            })
    
                    messages.append({"role": "user", "content": tools_results})
    
    
                else:
    
                    return response.content[0].text   

        finally: 
            await mcp_executor.exit_stack.aclose()