from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain import hub
import requests
import json


@tool
def personal_details_based_on_name(name: str) -> int:
    """This method predicts the age, gender and the nationality of a person
    based on their name using 3 APIs"""

    response = {}

    r1 = requests.get('https://api.agify.io?name={}'.format(name))
    age_response = json.loads(r1.content.decode("utf-8"))
    response['age'] = age_response['age']

    r2 = requests.get('https://api.genderize.io/?name={}'.format(name))
    gender_response = json.loads(r2.content.decode("utf-8"))
    response['gender'] = gender_response['gender']

    r3 = requests.get('https://api.nationalize.io?name={}'.format(name))
    nationality_response = json.loads(r3.content.decode("utf-8"))
    response['nationality'] = nationality_response['country'][0]['country_id']

    return response

if __name__ == '__main__':
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [personal_details_based_on_name]
    llm_with_tools = llm.bind_functions(tools)

    # Refer to https://smith.langchain.com/hub/hwchase17/openai-tools-agent
    system_prompt = hub.pull("hwchase17/openai-functions-agent")

    agent = create_openai_functions_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    user_prompt = "Tell me more about Davide"
    response = agent_executor.invoke({"input": user_prompt})

    print(response['output'])