from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
# from crewai.project import CrewBase, agent, crew, task


class AgentCrew:
    """Agent crew"""
    def __init__(self, agent, llm, tools, task, model_name="gpt-3.5-turbo"):
        self.agents = agent
        self.llm = llm
        self.tools = tools
        self.model_name = model_name
    
    def define_agent(self):
        for agent in self.agents:
            for tool in self.tools:
                tool = self.define_tool(tool)
            agent = Agent(
                role=agent.role,
                goal=agent.goal,
                backstory=agent.backstory,
                allow_delegation=True,
                llm=self.llm,
                tools= tool

            )
            return agent
    def define_tool(self, tools):
        pass
    def define_task(self):
        
        pass

    def define_crew(self):
        pass