from typing import Any,Dict
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import GraphState
from dotenv import load_dotenv


load_dotenv()

web_search_tool = TavilySearchResults(max_results=3)

def web_search_node(state: GraphState)->Dict[str,Any]:
    print("--Web Search--")
    question = state["question"]
    documents = state["documents"]

    tavily_results = web_search_tool.invoke({"query":question})
    joined_tavily_result = "\n".join([
        tavily_result["content"] for tavily_result in tavily_results
    ])
    web_results = Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]

    return {"question":question,"documents":documents}




