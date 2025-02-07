from typing import Any, Dict
from ingestion import retriever
from graph.state import GraphState 

def retrieve(state: GraphState)->Dict[str,Any]:
    print("--Retrieve--")
    question = state["question"]

    documents = retriever.invoke(question)
    return {"documents": documents,"question":question}



