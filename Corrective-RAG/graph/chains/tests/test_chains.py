from dotenv import load_dotenv
from graph.chains.retrieval_grader import retrieval_grader,GradeDocuments
from ingestion import retriever

load_dotenv()

def test_retrieval_grader_answer_yes()->None:
    question = "Agent memory"
    docs = retriever.invoke(question)
    doc_text = docs[0].page_content
    print("----Doc Text: ",doc_text)

    res:GradeDocuments = retrieval_grader.invoke(
        {"document": doc_text,"question":question}
    )

    assert res.binary_score == "yes"

def test_retrieval_grader_answer_no()->None:
    question = "How to make pizza"
    docs = retriever.invoke(question)
    doc_text = docs[0].page_content

    res:GradeDocuments = retrieval_grader.invoke(
        {"document": doc_text,"question":question}
    )

    assert res.binary_score == "no"
