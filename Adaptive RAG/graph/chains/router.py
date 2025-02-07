from typing import Literal
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_openai import ChatOpenAI

load_dotenv()

class RouteQuery(BaseModel):
    """Route a user query to most relevant data source"""
    datasource:Literal["vectorstore","websearch"] = Field(
        ...,
        description= "Given a user question choose to route it to web search or vectorstore."
    )

llm = ChatOpenAI(temperature=0)

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """you are an expert at routing a user question to a vectorstore or web search.
            The vectorstore contains documents related to agents,prompt engineering and adversial attacks.
         """

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system),
        ("human","{question}")
    ]
)

question_router = route_prompt | structured_llm_router
