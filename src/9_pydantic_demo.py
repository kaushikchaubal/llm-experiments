from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: str = Field(description="sentiment of text, should be `Positive sentiment`, `Negative sentiment`, "
                                       "or `Neutral sentiment`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")


if __name__ == '__main__':
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    tagging_functions = [convert_to_openai_function(Tagging)]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Think carefully, and then tag the text as instructed"),
        ("user", "{input}")
    ])

    model_with_functions = model.bind_tools(tagging_functions, tool_choice="auto")

    tagging_chain = prompt | model_with_functions

    user_prompt = """India wicketkeeper Rishabh Pant has been passed fit to play in the Indian Premier League (IPL) 
    after a 14-month absence from cricket.

        Pant, 26, has not played since being injured in a serious car accident in December 2022.
        
        It has been confirmed that Pant will play for Delhi Capitals in the upcoming IPL season, which starts on 22 
        March.
        
        Should Pant show he can keep wicket well, he could feature in India's squad for the Men's T20 World Cup in June.
        
        The Board of Control for Cricket in India (BCCI) said in a statement posted on X: "After undergoing an 
        extensive 14-month rehab and recovery process, following a life-threatening road mishap on December 30th, 
        2022, Rishabh Pant has now been declared fit as a wicketkeeper batter for the upcoming TATA IPL 2024."""

    response = tagging_chain.invoke({"input": user_prompt})

    print(response.additional_kwargs['tool_calls'][0]['function']['arguments'])


