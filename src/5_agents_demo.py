from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain import hub


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


if __name__ == '__main__':
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [get_word_length]
    llm_with_tools = llm.bind_tools(tools)

    # Refer to https://smith.langchain.com/hub/hwchase17/openai-tools-agent
    system_prompt = hub.pull("hwchase17/openai-functions-agent")

    agent = create_openai_functions_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    user_prompt = "How many letters are there in the word blaaaaah?"
    response = agent_executor.invoke({"input": user_prompt})

    print(response['output'])

    user_prompt = "Translate the spanish word 'Amigo' to English"
    response = agent_executor.invoke({"input": user_prompt})

    print(response['output'])
