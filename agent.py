class Agent:
    def __init__(self, name, description, llm, tools, agent_type, model_name="gpt-3.5-turbo"):
        self.name = name
        self.description = description
        self.llm = llm
        self.tools = tools
        self.model_name = model_name
        self.agent_type = agent_type

    def create_agent(self):
        if self.agent_type == "OpenAI_Assistant":
            return self.create_openai_agent()
        elif self.agent_type == "ReAct":
            return self.create_react_agent()
        else:
            return self.create_agent_with_tools()

    def create_react_agent(self):
        pass

    def create_openai_agent(self):
        pass

    def create_agent_with_tools(self):
        pass