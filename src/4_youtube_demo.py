from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

if __name__ == '__main__':
    urls = ["https://www.youtube.com/watch?v=23DINwD33rA"]

    # Directory to save audio files
    save_dir = "../resources/yt-audios/"

    loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embedding_function)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    retrievalQA = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        verbose=True
    )

    prompt = ("Answers based on the provided context. Which car model is this review about? What is the overall "
              "summary about Nissan Juke? Tell me the top 3 positives and top 3 negatives")
    response = retrievalQA.invoke(prompt)

    print(response['result'])

