# llm-experiments

This repo that captures experiments with OpenAI models and other LLM-related frameworks

## How to run
1. To run `1_openai_api_demo.py`, set the OPENAI_API_KEY env variable
2. To run `2_langchain_demo.py`, set the OPENAI_API_KEY env variable
3. To run `3_pdf_demo.py`, set the OPENAI_API_KEY and the TOKENIZERS_PARALLELISM=false env variables
4. To run `4_youtube_demo.py`, set the OPENAI_API_KEY and the TOKENIZERS_PARALLELISM=false env variables
5. To run `5_agents_demo.py`, set the OPENAI_API_KEY env variable
6. To run `6_agents_with_external_apis_demo.py`, set the OPENAI_API_KEY env variable
7. To run `7_langgraph_demo.py`, set the OPENAI_API_KEY env variable
8. To run `8_langgraph_tavily_demo.py`, set the OPENAI_API_KEY and the TAVILY_API_KEY env variables

## 1_openai_api_demo - prompt and response
Prompt:
```commandline
I want you to greet how any first computer science program usually greets the world, followed with a smiley
```

Response:
```commandline
Hello World! :)
```

## 2_langchain_demo - prompt and response
Prompt:
```commandline
I want you to greet how any first computer science program usually greets the world, followed with a smiley
```

Response:
```commandline
Hello World! :)
```

## 3_pdf_demo - prompt and response

Prompt:
```commandline
"According to given context, create a list of the different ways a batsman can get out"
```

Response:
```commandline
Based on the provided context, here is a list of different ways a batsman can get out in cricket:

1. Run out
2. Caught
3. Obstructing the field
4. Stumped
5. Hit the ball twice
6. LBW (Leg Before Wicket)
7. Hit wicket

These are the various ways a batsman can be dismissed according to the Laws of Cricket 2017 Code.
```

## 4_youtube_demo - prompt and response
Prompt:
```commandline
Answers based on the provided context. Which car model is this review about? What is the overall summary about Nissan Juke? Tell me the top 3 positives and top 3 negatives
```

Response:
```commandline
This review is about the Nissan Juke. The overall summary of the review is that the Nissan Juke has received updates and improvements, including a new engine, a bigger boot, and some styling upgrades. The reviewer mentions that the Juke has a unique and quirky design, good in-car storage, and a raised driving position that provides great visibility. However, the reviewer also mentions some negatives, such as the fidgety ride, lack of front-end grip in corners, and limited space in the back seats.

Top 3 positives:
1. Unique and quirky design
2. Good in-car storage
3. Raised driving position for better visibility

Top 3 negatives:
1. Fidgety ride
2. Lack of front-end grip in corners
3. Limited space in the back seats
```

## 5_agents_demo - prompts and responses

Prompt 1: Note that this prompt is **automagically calls** the custom `get_word_length` method that I defined
```commandline
How many letters are there in the word blaaaaah?
```

Response 1:
```commandline
There are 8 letters in the word "blaaaaah".
```

Prompt 2: Note that this prompt **does not** call the custom `get_word_length` method that I defined, even though the invoking logic is the same
```commandline
Translate the spanish word 'Amigo' to English
```

Response 2:
```commandline
The Spanish word "Amigo" translates to "Friend" in English.
```

## 6_agents_with_external_apis_demo.py - prompt and response
Prompt:
```commandline
Tell me more about Davide
```

Response
```commandline
Davide is estimated to be around 47 years old. The name Davide is most commonly associated with males, with a probability of 1.0. In terms of nationality, the name Davide is most likely associated with Italy (probability of 0.649), followed by Switzerland, Portugal, Belgium, and Luxembourg.

```

## 7_langgraph_demo - prompts and responses
Prompt:
```commandline
Tell me more about Davide
```

Response
```commandline
Davide is a male name and is most commonly associated with individuals who are around 47 years old. The name Davide is most likely of Italian origin, with a probability of 64.9%. It is also associated with other nationalities such as Swiss (8.4%), Portuguese (3.0%), Belgian (1.1%), and Luxembourgish (1.1%).

```


## 8_langgraph_tavily_demo - prompts and responses
Prompt:
```commandline
Whats's the weather in London like?
```

Response:
```commandline
The weather in London is currently transitioning to milder, wetter, and windier conditions. For more detailed and up-to-date information, you can visit the [Met Office website](https://www.metoffice.gov.uk/weather/forecast/gcpvj0v07).
```