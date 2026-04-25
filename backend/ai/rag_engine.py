from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import core.config as config
from ai.llm import get_llm, get_embeddings


def get_rag_chain():
    """
    Initializes the RAG chain by connecting the local vector DB with Llama3
    """
    # load llms
    embeddings = get_embeddings()
    llm = get_llm()
    
    # connect the vector db
    vector_db = Chroma(persist_directory=config.DB_DIR, embedding_function=embeddings)
    
    # retriever (top k set to 3)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # System Prompt
    system_prompt = (
        "You are a technical assistant."
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

    # create the chains
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

if __name__ == "__main__":
    # test
    chain = get_rag_chain()
    query = "What are the main safety instructions for this machine?"
    response = chain.invoke({"input": query})
    print("\nRESPONSE: ")
    print(response["answer"])