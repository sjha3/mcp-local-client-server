import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from Agents.Agents_with_tools import Agents_with_tools
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.ui import Console
from typing import Sequence
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from autogen_ext.tools.mcp import mcp_server_tools  # Adjust import path as needed
from mcp import ClientSession


from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        #self.exit_stack = AsyncExitStack()
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_endpoint=os.getenv("azure_endpoint"),
            azure_deployment=os.getenv("azure_deployment"),
            api_version=os.getenv("api_version"),
            api_key=os.getenv("api_key"),
            model=os.getenv("azure_model_name"),    
        )
        self.team_agents = None
        self.tools_ = []
        self.agents = Agents_with_tools()
            
    # methods will go here
    
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        print("Connecting to MCP server...")
                     
        #================ Get tools using Autogen Format of Agent ================#
        server_params_autogen = StdioServerParams(
            command="python",
            args=[server_script_path],
            env=None,
            read_timeout_seconds=30
        )
        # Get tools in OpenAI function-calling format
        self.tools_ = await mcp_server_tools(server_params_autogen)
        
        #Create agent team with the tools
        await self.agents.create_agent_team(self.tools_)        
    
    
    async def start_chat(self):
        print("**** Starting chat ****")
        
        #print(self.tools_)                
        
        while True:
            try:
                task = input("Please enter a task: ")
                if task.lower() == "exit":
                    print("**** Exiting chat...")
                    break
                print("Running task:", task)
                await Console(self.agents.team_agents.run_stream(task = task))
                
            except Exception as e:
                print(f"Error occurred: {e}")
                task = input("Please enter a new task: ")
        
        
    async def close(self):
        await self.exit_stack.aclose()