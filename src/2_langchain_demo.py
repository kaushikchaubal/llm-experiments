from langchain_openai import ChatOpenAI

if __name__ == '__main__':
    llm = ChatOpenAI()

    prompt = """
            I want you to greet how any first 
            computer science program usually greets the world, 
            followed with a smiley
        """

    response = llm.invoke(prompt)

    print(response.content)