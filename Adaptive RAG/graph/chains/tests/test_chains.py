from dotenv import load_dotenv
from graph.chains.retrieval_grader import retrieval_grader,GradeDocuments
from ingestion import retriever
from pprint import pprint
from graph.chains.generation import generation_chain
from graph.chains.hallucination_grader import GradeHallucinations,hallucination_grader
from graph.chains.router import question_router,RouteQuery

load_dotenv()

def test_retrieval_grader_answer_yes()->None:
    question = "Agent memory"
    docs = retriever.invoke(question)
    flag = "no"
    for doc in docs:
        res:GradeDocuments = retrieval_grader.invoke(
            {"document": doc.page_content,"question":question}
        )
        if res.binary_score == "yes":
           flag="yes"

    assert flag == "yes"

def test_retrieval_grader_answer_no()->None:
    question = "How to make pizza"
    docs = retriever.invoke(question)
    doc_text = docs[0].page_content

    res:GradeDocuments = retrieval_grader.invoke(
        {"document": doc_text,"question":question}
    )

    assert res.binary_score == "no"

def test_generation_chain()->None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs,"question":question})
    pprint(generation)

def test_hallucination_grader_answer_yes()->None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context":docs,"question":question})

    res: GradeHallucinations = hallucination_grader.invoke({"documents":docs,"generation":generation})

    assert  res.binary_score

def test_hallucination_grader_answer_no()->None:
    question = "How to make pizza"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context":docs,"question":question})

    res: GradeHallucinations = hallucination_grader.invoke({"documents":docs,"generation":generation})

    assert not res.binary_score

def test_router_to_vectorstore()->None:
    question = "agent memory"

    res:RouteQuery = question_router.invoke({"question":question})
    assert res.datasource == "vectorstore"

def test_router_to_websearch()->None:
    question = "how to make pizza"

    res:RouteQuery = question_router.invoke({"question":question})
    assert res.datasource == "websearch"