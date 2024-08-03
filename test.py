from crewai import Agent, Crew, Task, Process
from crewai_tools import tool
from typing import List, Dict, Any, Union
import json
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

class AgentCrew:
    """Agent crew"""
    def __init__(self, agents: List[Dict[str, str]], tools: List[Dict[str, Any]], tasks: List[Dict[str, str]], model_name: str = "gpt-3.5-turbo"):
        self.agents = agents
        self.tools = tools
        self.tasks = tasks
        self.model_name = model_name
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        # load_dotenv()
        return AzureChatOpenAI(
            azure_endpoint="https://brimink.openai.azure.com/",
            api_key="922483b735a44b5782a526874a693cea",
            api_version="2024-02-15-preview",
            azure_deployment=self.model_name,
            
        )

    def define_agent(self) -> List[Agent]:
        defined_agents = []
        for agent_info in self.agents:
            agent_tools = [self.define_tool(tool) for tool in self.tools]
            agent = Agent(
                role=agent_info['role'],
                goal=agent_info['goal'],
                backstory=agent_info['backstory'],
                allow_delegation=True,
                llm=self.llm,
                # tools=agent_tools
            )
            defined_agents.append(agent)
        return defined_agents

    def define_tool(self, tool_info: Dict[str, Any]):
        @tool(tool_info['name'])
        def custom_tool(question: str) -> str:
            """Clear description for what this tool is useful for."""
            return tool_info['function'](question)
        
        return custom_tool

    def define_task(self) -> List[Task]:
        defined_tasks = []
        defined_agents = {agent.role: agent for agent in self.define_agent()}
        
        for task_info in self.tasks:
            task = Task(
                description=task_info['description'],
                expected_output=task_info['expected_output'],
                agent=defined_agents[task_info['agent']]
            )
            defined_tasks.append(task)
        return defined_tasks

    def define_crew(self) -> Crew:
        agents = self.define_agent()
        tasks = self.define_task()
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=2,
            manager_llm=self.llm
        )

    def kickoff(self, inputs: Dict[str, Any] = None) -> Any:
        crew = self.define_crew()
        result = crew.kickoff(inputs=inputs)
        return result

    def print_task_output(self, task_output: Union[str, Task]):
        if isinstance(task_output, str):
            print("Task Output:")
            print(task_output)
        else:
            print(f"Task Description: {task_output.description}")
            print(f"Task Summary: {task_output.summary}")
            print(f"Raw Output: {task_output.raw}")
            if hasattr(task_output, 'json_dict') and task_output.json_dict:
                print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
            if hasattr(task_output, 'pydantic') and task_output.pydantic:
                print(f"Pydantic Output: {task_output.pydantic}")

print(f"Model Name:")


def search_function(query: str) -> str:
    """Search for information on the internet"""
    # Implement your search function here
    return "openai launchs gpt 8, plus LLAMA 4 from meta"

agents = [
    {
        "role": "Research Agent",  # This should match the 'agent' in tasks
        "goal": "Find and summarize the latest AI news",
        "backstory": "Expert in gathering and analyzing information",
    },
    {
        "role": "Reporting Analyst",
        "goal": "Analyze and report on AI news",
        "backstory": "Expert in analyzing and reporting on AI news",
    }
    # Add more agents as needed
]

tools = [
    {
        "name": "search_tool",
        "description": "Search for information on the internet",
        "function": search_function,  # You need to define this function
    }
    # Add more tools as needed
]

tasks = [
    {
        "description": "Find and summarize the latest AI news",
        "expected_output": "A bullet list summary of the top 5 most important AI news",
        "agent": "Research Agent"  # This should match the 'role' in agents
    },
    {
        "description": "Analyze and report on AI news",
        "expected_output": "An analysis of the top 5 most important AI news",
        "agent": "Reporting Analyst"  # This should match the 'role' in agents
    }
    # Add more tasks as needed
]

crew = AgentCrew(agents, tools, tasks, model_name="gpt-4o")
result = crew.kickoff(inputs={"input": "AI news"})
crew.print_task_output(result)

