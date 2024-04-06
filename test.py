from crewai import Agent, Crew, Task
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

import os

os.environ["TAVILY_API_KEY"] = "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"
llm = ChatOpenAI(temperature=0.7, openai_api_key="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")

agent = Agent(
      role='financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
      verbose=True,
      llm=llm,
      tools=[
        YahooFinanceNewsTool(),
        TavilySearchResults(),

      ]
  )


research_task = Task(
  description=(
    """Research stock price of {company}"""
  ),
  expected_output='information on the stock',

  agent=agent,
)

crew = Crew(
  agents=[agent],
  tasks=[research_task],

)

result = crew.kickoff(inputs={'company': 'what is the current stock price of AAPL'})
print(result)