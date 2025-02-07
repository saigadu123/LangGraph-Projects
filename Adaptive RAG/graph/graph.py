from dotenv import load_dotenv
from langgraph.graph import END,StateGraph
from graph.consts import RETRIEVE,GRADE_DOCUMENTS,WEB_SEARCH,GENERATE,WEB_SEARCH_DIRECT
from graph.nodes import retrieve,grade_documents,web_search_node_direct,generate
from graph.state import GraphState
from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import RouteQuery,question_router
load_dotenv()


def decide_to_generate(state):
    print("--ASSESS GRADED DOCUMENTS--")

    if state["web_search"]:
        print(
            "--DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION"
        )
        return WEB_SEARCH_DIRECT
    else:
        print("---DECISION: GENERATE---")
        return GENERATE 
    

def grade_generation_grounded_in_documents_and_question(state:GraphState)->str:
    print("--CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents":documents,"generation":generation}
    )

    if hallucination_grade := score.binary_score:
        print("--DECISION : GENERATION IS GROUNDED IN DOCUMENTS---")
        print("-- GRADE GENERATION Vs QUESTION---")
        score = answer_grader.invoke({"question":question,"generation":generation})
        if answer_grade := score.binary_score:
            print("-- DECISION: GENERATION ADDRESSESS QUESTION---")
            return "useful"
        else:
            print("----DECISION: GENERATION DOES NOT ADDRESSESS QUESTION")
            return "not useful"
    else:
        print("--DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS")
        return "not supported"
    
def route_question(state: GraphState)->str:
    print("---ROUTE QUESTION----")
    question = state["question"]
    source:RouteQuery = question_router.invoke({"question":question})
    if source.datasource == "websearch":
        print("--ROUTE QUESTION TO WEB SEARCH---")
        return WEB_SEARCH_DIRECT
    else:
        print("---ROUTE QUESTION TO VECTOR STORE---")
        return RETRIEVE

    
workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE,retrieve)
workflow.add_node(GRADE_DOCUMENTS,grade_documents)
workflow.add_node(WEB_SEARCH_DIRECT,web_search_node_direct)
workflow.add_node(GENERATE,generate)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE,GRADE_DOCUMENTS)

workflow.set_conditional_entry_point(
    route_question,
    path_map={
        WEB_SEARCH_DIRECT : WEB_SEARCH_DIRECT,
        RETRIEVE : RETRIEVE
    }
)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    path_map = {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEB_SEARCH_DIRECT
    }
)

workflow.add_edge(WEB_SEARCH_DIRECT,GENERATE)
workflow.add_edge(GENERATE,END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")


