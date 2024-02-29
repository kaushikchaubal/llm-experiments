from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain import hub
import requests
import json


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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [age_of_person, gender_of_person, nationality_of_person]
    llm.bind_functions(tools)

    # Refer to https://smith.langchain.com/hub/hwchase17/openai-tools-agent
    system_prompt = hub.pull("hwchase17/openai-functions-agent")

    agent = create_openai_functions_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    user_prompt = "Tell me more about Davide"
    response = agent_executor.invoke({"input": user_prompt})

    print(response['output'])
