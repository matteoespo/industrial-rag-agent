from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os

# Configuration
DB_DIR = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_rag_chain():
    """
    Initializes the RAG chain by connecting the local vector DB with Llama3.
    """
    # Load the existing vector database
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    # Setup the retriever (searches for the top 3 most relevant chunks)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # Initialize the Local LLM (Llama3)
    llm = ChatOllama(model=LLM_MODEL, temperature=0, base_url=OLLAMA_BASE_URL) # Temperature is set to 0 for consistent, factual technical answers

    # Define the System Prompt (tells the AI how to behave and forces it to use only provided context)
    system_prompt = (
        "You are a technical assistant for industrial machinery."
        "Use the following pieces of retrieved context to answer the question."
        "If you don't know the answer based on the context, say that you don't know."
        "Keep the answer concise and professional."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create the chains
    # stuff_documents_chain: takes retrieved docs and "stuffs" them into the prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # retrieval_chain: coordinates the retrieval process and the answering process
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

if __name__ == "__main__":
    # CLI test
    print("Initializing RAG Engine...")
    chain = get_rag_chain()
    
    query = "What are the main safety instructions for this machine?"
    print(f"Querying: {query}")
    
    response = chain.invoke({"input": query})
    print("\n--- RESPONSE ---")
    print(response["answer"])