import chainlit as cl
from langchain_core.tools import tool
from chainlit.cli import run_chainlit


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


@cl.on_message
async def main(message: cl.Message):
    # Call the tool
    length = get_word_length(message.content)

    # Send the final answer.
    await cl.Message(content="Word length for {} is {}".format(message.content, length)).send()


if __name__ == "__main__":
    run_chainlit(__file__)
