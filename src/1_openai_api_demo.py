from openai import OpenAI

if __name__ == '__main__':
    client = OpenAI()
    prompt = """
        I want you to greet how any first 
        computer science program usually greets the world, 
        followed with a smiley
    """

    messages = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        stream=True
    )

    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")