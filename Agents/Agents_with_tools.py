from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.ui import Console
from typing import Sequence
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient


class Agents_with_tools():
    
    def __init__(self):
        load_dotenv(override=True)  # Load environment variables from .env file
        print("Azure end point:", os.getenv("azure_endpoint"))
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_endpoint=os.getenv("azure_endpoint"),
            azure_deployment=os.getenv("azure_deployment"),
            api_version=os.getenv("api_version"),
            api_key=os.getenv("api_key"),
            model= "gpt-4o-2024-11-20"#enhance token/cost estimation using it instead of gpt-4o  
        )
        self.team_agents = None

    async def create_agent_team(self, mcp_tools):
        text_mention_termination = TextMentionTermination("TERMINATE")
        max_messages_termination = MaxMessageTermination(25)
        termination = text_mention_termination | max_messages_termination
        print("**** Create review agent ****")
        review_agent = AssistantAgent(
            name = "ReviewAgent",
            model_client = self.model_client,
            system_message= """
            You are a helpful agent which manages review object
            You should be able to create a review and get details of a review
            To get all the reviews, use kusto query as GetReviewsTest
            Schema of the review object is as follows:
                ReviewId: Unique identifier for the review
                ReviewName: Name of the review
                WorkloadId: Unique identifier for the workload associated with the review
                WorkloadName: Name of the workload associated with the review
                Owner: Email of the owner of the review
                ModifiedOn: Timestamp of when the review was last modified
                IsDelete: Boolean indicating if the review is deleted
            """,
            tools = mcp_tools
        )
        print("**** Create finance agent ****")
        finance_agent = AssistantAgent(
            name = "FinanceAgent",
            model_client = self.model_client,
            system_message= """
            You are a helpful agent which manages financial data
            """,
            tools = mcp_tools
        )
        print("=**** Create file agent ****")
        file_agent = AssistantAgent(
            name = "FileAgent",
            model_client = self.model_client,
            system_message= """
            You are a helpful agent which reads data from csv and parquet files
            """,
            tools = mcp_tools
        )
        
        response_agent = AssistantAgent(
            name="ResponseAgent",
            description="An agent that formats and sends the final response to the user.",
            model_client=self.model_client,
            system_message="""You are a response agent. 
            Your task is to format and send the final response to the user.
            Always end the conversation with 'TERMINATE'.
            
            Always end your response with 'TERMINATE' to indicate the conversation is complete.
            """,
        )
        
        planning_agent = AssistantAgent(
            "PlanningAgent",
            model_client=self.model_client,
            description="""
                An agent that plans tasks based on user requests.
                It should break down tasks and delegate them to appropriate agents.
                """,
            system_message=
                """
                    You are a planning agent. 
                    Your task is to break down user requests into smaller tasks and delegate them to appropriate agents.
                    Your team members are
                    - FileAgent: Acts on csv and oarquet files
                    - FinanceAgent: Provides financial data of stocks.
                    - ReviewAgent: Manages review objects.                    
                    - ResponseAgent: Responsible for responding to the user with the final response.
                    
                    You only plan and delegate tasks, you do not execute them.
                    
                    When assignning tasks to agents, use the following format:
                    1. <agent>: <task>
                    
                    Once a task is completed by another agent, delegate the response to the **ResponseAgent**
                    to format and send the final response to the user.
                """,
        )
        
        def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
            if messages[-1].source != planning_agent.name:
                return planning_agent.name
            return None
        
        self.team_agents = SelectorGroupChat([review_agent,
                                  finance_agent,
                                  file_agent,
                                  planning_agent,
                                  response_agent],
                                 model_client=self.model_client, 
                                 selector_func=selector_func,
                                 termination_condition=termination,
                                 allow_repeated_speaker=True)
        print("**** Agent team created successfully ****")
    