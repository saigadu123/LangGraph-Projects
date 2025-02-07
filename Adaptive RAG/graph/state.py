from typing import Annotated
from typing_extensions import TypedDict
from operator import add


class GraphState(TypedDict):
    """ 
    Represents the state of the Graph

    Attributes:
      question : question
      generation: LLM Generation
      Web_search: Whether to add search
      documents: List of documents
    
    """
    question : Annotated[str,add]
    generation: str
    web_search: bool
    documents: Annotated[list[str],add]