from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.utils.function_calling import convert_to_openai_function
from langgraph.prebuilt import ToolExecutor
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.messages import FunctionMessage
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain.agents import tool
import requests


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    # If there is no function call, then we finish
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define the function that calls the model
def call_agent(state):
    messages = state['messages']
    response = agent.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
def call_tool(state):
    messages = state['messages']
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),
    )
    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(content=str(response), name=action.tool)
    # We return a list, because this will get added to the existing list
    return {"messages": [function_message]}


@tool
def age_of_person(name: str):
    """This method predicts the age of a person based on their name"""

    r1 = requests.get('https://api.agify.io?name={}'.format(name))
    age_response = json.loads(r1.content.decode("utf-8"))
    return age_response

@tool
def gender_of_person(name: str):
    """This method predicts the gender of a person based on their name"""

    r2 = requests.get('https://api.genderize.io/?name={}'.format(name))
    gender_response = json.loads(r2.content.decode("utf-8"))
    return gender_response

@tool
def nationality_of_person(name: str):
    """This method predicts the nationality of a person based on their name"""

    r3 = requests.get('https://api.nationalize.io?name={}'.format(name))
    nationality_response = json.loads(r3.content.decode("utf-8"))
    return nationality_response


if __name__ == '__main__':
    tools = [age_of_person, gender_of_person, nationality_of_person]

    tool_executor = ToolExecutor(tools)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)

    agent = llm.bind_functions(tools)

    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_agent)
    workflow.add_node("action", call_tool)

    # # Set the entrypoint as `agent`
    # # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        conditional_edge_mapping={
            "continue": "action",
            "end": END
        }
    )

    workflow.add_edge('action', 'agent')
    app = workflow.compile()

    inputs = {"messages": [HumanMessage(content="Tell me more about Davide")]}

    for output in app.stream(inputs):
        for key, value in output.items():
            if key == 'agent':
                response = value['messages'][0].content
                print(response)
