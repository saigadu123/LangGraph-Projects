from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(temperature=0)

class GradeDocuments(BaseModel):
    """ Binary score for relevance check for the retrieved documents """

    binary_score: str = Field(
        description = "Documents are relevant to the question, 'yes' or 'no' "
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """ You are a grader assessing relevance of a retrieved document to a user question.\n
            If the retrieved documents are someover related to the question, then that document is relavant to the question.
            
          """

grade_prompt = ChatPromptTemplate.from_messages(
    [
    ("system",system),
    ("human","Retrieved documents:\n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader