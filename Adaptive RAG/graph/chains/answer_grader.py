from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class GradeAnswer(BaseModel):
    binary_score: bool = Field("Answer addresses the question, 'yes' or 'no")

llm = ChatOpenAI(temperature=0)

structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """ You are a grader assessing whether the answer addresses / resolves a question \n 
             Give a binary score 'yes' or 'no'. 'yes' means that the answer resolves the question.
           """

answer_grader_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system),
        ("human","User question: \n\n {question} \n\n LLM Generation:{generation}"),
    ]
)

answer_grader:RunnableSequence = answer_grader_prompt | structured_llm_grader




