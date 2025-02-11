from dotenv import load_dotenv
import operator
from typing import Annotated,Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

load_dotenv()

class State(TypedDict):
    aggregate: Annotated[list,operator.add]


class ReturnNodeValue:
    def __init__(self, node_secret:str):
        self._value = node_secret

    def __call__(self,state:State)->Any:
        import time
        time.sleep(2)
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate":[self._value]}

builder = StateGraph(State)
builder.add_node("a",ReturnNodeValue("I am 'A'"))
builder.add_edge(START,"a")
builder.add_node("b",ReturnNodeValue("I am 'B'"))
builder.add_node("c",ReturnNodeValue("I am 'C'"))
builder.add_node("b2",ReturnNodeValue("I am 'B2'"))
builder.add_node("d",ReturnNodeValue("I am 'd'"))
builder.add_edge("a","b")
builder.add_edge("a","c")
builder.add_edge("b","b2")
builder.add_edge(["b2","c"],"d")

builder.add_edge("d",END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async_graph_fan-in&fan-out.png")


if __name__ == "__main__":
    print("Hello Async Graph")
    graph.invoke({"aggregate":[]},{"configurable":{"thread_id":"foo"}})