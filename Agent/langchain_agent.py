from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"


def invoke_agent(agent_args, input):
    tools = []
    if agent_args.web_search is True:
        tools.append(TavilySearchResults())

    prompt = hub.pull("hwchase17/openai-tools-agent")
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

    # Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    res = agent_executor.invoke({"input": input})
    return res