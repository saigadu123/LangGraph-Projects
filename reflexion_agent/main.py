from dotenv import load_dotenv

from typing import List
from langchain_core.messages import BaseMessage,ToolMessage 
from langgraph.graph import END,MessageGraph
from chains import first_responder,revisor
from tool_executor import execute_tools


load_dotenv()

DRAFT = "draft"
EXECUTE_TOOLS = "execute_tools"
REVISE = "revise"


MAX_ITERATIONS = 2

builder = MessageGraph()
builder.add_node(DRAFT,first_responder)
builder.add_node(EXECUTE_TOOLS,execute_tools)
builder.add_node(REVISE,revisor)
builder.add_edge(start_key="draft",end_key="execute_tools")
builder.add_edge(start_key="execute_tools",end_key="revise")

def event_loop(state: List[BaseMessage])->str:
    count_tool_visits = sum(isinstance(item,ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations>MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges(REVISE, event_loop)
builder.set_entry_point("draft")
graph = builder.compile()

print(graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    print("Reflextion Agent")
    res =  graph.invoke("Write about AI-powered SOC / autonomous SOC problem domain, list startups that do that and raised capital")
    print("Final answer:  ",res[-1].tool_calls[0]["args"]["answer"])