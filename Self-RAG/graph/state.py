from typing import List,TypedDict




class GraphState(TypedDict):
    """ 
    Represents the state of the Graph

    Attributes:
      question : question
      generation: LLM Generation
      Web_search: Whether to add search
      documents: List of documents
    
    """
    question : str 
    generation: str
    web_search: bool
    documents: List[str]