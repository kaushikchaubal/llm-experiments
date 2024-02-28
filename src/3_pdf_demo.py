from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

if __name__ == '__main__':
    loader = PyPDFLoader("https://www.lords.org/getattachment/MCC/All-Laws/2nd-Edition-of-the-2017-code-2019.pdf")
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

    prompt = "According to given context, create a list of the different ways a batsman can get out"
    response = retrievalQA.invoke(prompt)

    print(response['result'])
