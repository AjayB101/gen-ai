from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph,START
from chains import generation_chain,reflectionchain
from IPython.display import Image,Markdown
load_dotenv()

REFLECT="reflect"
GENERATE="generate"
graph=MessageGraph()

def generate(state):
   return generation_chain.invoke({"messages":state})

def reflect(state):
    res=reflectionchain.invoke({"messages":state})
    return [HumanMessage(content=res.content)]

def condition(state):
    if len(state)>3:
        return END
    return REFLECT

graph.add_node(GENERATE,generate)
graph.add_node(REFLECT,reflect)
graph.add_edge(START,GENERATE)
graph.add_conditional_edges(GENERATE,condition)
graph.add_edge(REFLECT,GENERATE)
app=graph.compile()
res=app.invoke(HumanMessage(content="AI Agents taking over content creation"))
print(res)
