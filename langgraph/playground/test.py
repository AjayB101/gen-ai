from dotenv import load_dotenv
from langgraph.playground.agent import Agent
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import TavilySearchResults

load_dotenv()

# Initialize your custom agent
agent = Agent()
llm = agent.get_agent()

# Set up search tool
search_tool = TavilySearchResults(max_results=5, search_depth="basic")
tools = [search_tool]

# Initialize the agent executor
agent_executor = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,  # Increased from 2 to allow completion
    return_intermediate_steps=True
)

# Create a more specific prompt
prompt = """
You are a news app you to tell the users questions 
once you got the observation stop the llm

user query:

Whats the current status of iran israel war 
"""

# Execute the agent
try:
    result = agent_executor.invoke({"input": prompt})
    print("Final Answer:")
    print(result["output"])
except Exception as e:
    print(f"Error: {e}")