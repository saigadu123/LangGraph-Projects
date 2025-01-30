from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,ToolMessage,HumanMessage,AIMessage
from typing import List 
from schemas import AnswerQuestion,Reflection
from chains import json_parser
from langgraph.prebuilt import ToolInvocation,ToolExecutor
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from collections import defaultdict
import json

load_dotenv()

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search,max_results=5)
tool_executor = ToolExecutor([tavily_tool])

def execute_tools(state: List[BaseMessage])->List[ToolMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls  = json_parser.invoke(tool_invocation)
    print("Parsed tool calls: ",parsed_tool_calls)
    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(ToolInvocation(
                tool= "tavily_search_results_json",
                tool_input= query
            ))
        ids.append(parsed_call["id"])

    outputs = tool_executor.batch(tool_invocations)
    
    outputs_map = defaultdict(dict)
    for id_,output,invocation in zip(ids,outputs,tool_invocations):
        outputs_map[id_][invocation.tool_input] = output

    tool_messages = []
    for id_,mapped_output in outputs_map.items():
        tool_messages.append(ToolMessage(content = json.dumps(mapped_output),tool_call_id = id_))

    return tool_messages


if __name__ == "__main__":
    print("Tool Executor start")
    human_message = HumanMessage(
        content = "Write about AI powered SOC/ autonomous SOC problem domain,"
        "List startups that do that and raised capital"
    )
    answer = AnswerQuestion(
        answer= "",
        reflection= Reflection(missing = "",superfluous=""),
        search_queries= [
            "AI-powered SOC startups funding",
            "AI SOC problem domain specifics",
            "Technologies used by AI-powered SOC startups"
        ],
        id = "call_hiudgyufdywdftfduiuguyyfdyugyud"
    )

    raw_res = execute_tools(
        state = [
        human_message,
        AIMessage(
            content = "",
            tool_calls = [
                {
                    "name": AnswerQuestion.__name__,
                    "args" : answer.dict(),
                    "id" : "call_hiudgyufdywdftfduiuguyyfdyugyud"
                }
            ],
        ),
        ]
    )
    print("--------------------")
    print(raw_res)
