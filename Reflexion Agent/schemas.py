from typing import List 
from langchain_core.pydantic_v1 import BaseModel,Field 


class Reflection(BaseModel):
    missing: str = Field(description= "Critique of what it is missing")
    superfluous: str = Field(description = "Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    answer: str = Field(description = "~250 word detailed answer to the question")
    reflection: Reflection = Field(description = "Your reflection on initial answer")
    search_queries: List[str] = Field(
        description = "1-3 search queries for researching improvements to address the critique of your current answer."
    )

class ReviseAnswer(BaseModel):
    answer: str = Field(description="~250 word detailed answer to the question ")
    reflection: Reflection = Field(description="your reflection on tool genearated answer")
    search_queries: List[str] = Field(
        description = "1-3 search queries for researching improvements to address the critique of your current answer."
    )