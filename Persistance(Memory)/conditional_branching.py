from dotenv import load_dotenv
import operator
from typing import Annotated,Any,Sequence
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

load_dotenv()

class State(TypedDict):
    aggregate: Annotated[list,operator.add]
    which : str


class ReturnNodeValue:
    def __init__(self, node_secret:str):
        self._value = node_secret

    def __call__(self,state:State)->Any:
        import time
        time.sleep(2)
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate":[self._value]}

def route_bc_or_cd(state:State)->Sequence[str]:
    if state["which"] == "cd":
        return ["c","d"]
    return ["b","c"]

intermediates = ["b","c","d"]

builder = StateGraph(State)
builder.add_node("a",ReturnNodeValue("I am 'A'"))
builder.add_edge(START,"a")
builder.add_node("b",ReturnNodeValue("I am 'B'"))
builder.add_node("c",ReturnNodeValue("I am 'C'"))
builder.add_node("d",ReturnNodeValue("I am 'D'"))
builder.add_node("e",ReturnNodeValue("I am 'E'"))

builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    intermediates
)

for node in intermediates:
    builder.add_edge(node,"e")

builder.add_edge("e",END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="conditional_graph.png")


if __name__ == "__main__":
    print("Hello Async Graph")
    graph.invoke({"aggregate":[],"which":"cd"},{"configurable":{"thread_id":"foo"}})